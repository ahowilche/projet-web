# microfinance_project/gmycom/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction as db_transaction
from django.db.models import Sum, Count, Q, F, Prefetch
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages # Pour les messages flash
from django.http import JsonResponse # Importé pour les réponses JSON
from django.forms import inlineformset_factory # Importé pour les formsets
from datetime import date, timedelta
from decimal import Decimal
from django.db.models.functions import Coalesce

from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.units import cm
from reportlab.lib import colors

from django.views.decorators.http import require_POST, require_GET 
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format

import os
from io import BytesIO
import json

import requests
from django.core.files.storage import default_storage
from PIL import Image as PILImage

# Importation du modèle User par défaut de Django
from django.contrib.auth.models import User, Group 

from .models import Client, Compte, Mouvement, Credit, Remboursement, HistoriqueTransaction, ClientDocument # Ajout de ClientDocument
from .forms import AgentLoginForm, ClientForm, CompteForm, MouvementForm, CreditForm, RemboursementForm # Assurez-vous que ClientForm est importé

# Définition du formset pour ClientDocument (peut être déplacé dans forms.py si vous le préférez)
ClientDocumentFormSet = inlineformset_factory(Client, ClientDocument,
                                            fields=('type_document', 'fichier', 'description'),
                                            extra=1, # Nombre de formulaires vides à afficher initialement
                                            can_delete=True)


# --- Fonctions utilitaires pour les permissions ---
def is_admin_access(user):
    """Vérifie si l'utilisateur est un superutilisateur Django."""
    return user.is_authenticated and user.is_superuser

def is_agent_access(user):
    """
    Vérifie si l'utilisateur est authentifié et appartient au groupe 'Agents'.
    Les superutilisateurs ont également accès.
    """
    if not user.is_authenticated:
        return False
    # Si l'utilisateur est un superutilisateur, il a toujours accès
    if user.is_superuser:
        return True
    # Vérifie si l'utilisateur est dans le groupe 'Agents'
    return user.groups.filter(name='Agents').exists()


# --- Vues d'authentification ---

def agent_login(request):
    """
    Gère la connexion des agents.
    """
    if request.user.is_authenticated:
        return redirect('dashboard') # Redirige si déjà connecté

    if request.method == 'POST':
        form = AgentLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Vérifiez si l'utilisateur a le droit d'accéder à l'application (est un agent ou admin)
                if is_agent_access(user):
                    login(request, user)
                    messages.success(request, f"Bienvenue, {user.username} !")
                    return redirect('dashboard')
                else:
                    messages.error(request, "Vos identifiants sont valides, mais vous n'avez pas les permissions d'agent ou d'administrateur pour cette application.")
                    logout(request) # Déconnecte l'utilisateur s'il n'a pas le rôle requis
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = AgentLoginForm()
    return render(request, 'gmycom/login.html', {'form': form})

@login_required
def agent_logout(request):
    """
    Déconnexion de l'agent.
    """
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('login')

# --- Tableau de bord ---

@login_required
@user_passes_test(is_agent_access, login_url='login')
def dashboard(request):
    """
    Affiche le tableau de bord avec les statistiques clés.
    """
    total_clients = Client.objects.count()
    total_comptes = Compte.objects.count()
    total_epargne_solde = Compte.objects.filter(type_compte='epargne').aggregate(Sum('solde'))['solde__sum'] or Decimal('0.00')
    total_courant_solde = Compte.objects.filter(type_compte='courant').aggregate(Sum('solde'))['solde__sum'] or Decimal('0.00')
    
    # Crédits en cours et remboursés
    active_credits_count = Credit.objects.filter(status='ACTIVE').count()
    repaid_credits_count = Credit.objects.filter(status='REPAID').count()
    
    # Nouvelles métriques pour les crédits
    total_amount_granted_principal = Credit.objects.aggregate(Sum('amount_granted'))['amount_granted__sum'] or Decimal('0.00')
    total_expected_repayment_all_credits = Credit.objects.aggregate(Sum('total_expected_repayment'))['total_expected_repayment__sum'] or Decimal('0.00')
    total_amount_repaid_all_credits = Credit.objects.aggregate(Sum('amount_repaid'))['amount_repaid__sum'] or Decimal('0.00')

    # Transactions récentes (les 5 dernières)
    recent_transactions = HistoriqueTransaction.objects.order_by('-date_operation')[:5]

    # Préparation des variables de contexte pour le rôle de l'utilisateur
    is_admin_user = request.user.is_superuser
    is_agent_group = request.user.groups.filter(name='Agents').exists()

    context = {
        'total_clients': total_clients,
        'total_comptes': total_comptes,
        'total_epargne_solde': total_epargne_solde,
        'total_courant_solde': total_courant_solde,
        'active_credits_count': active_credits_count,
        'repaid_credits_count': repaid_credits_count,
        'total_amount_granted_principal': total_amount_granted_principal,
        'total_expected_repayment_all_credits': total_expected_repayment_all_credits,
        'total_amount_repaid_all_credits': total_amount_repaid_all_credits,
        'recent_transactions': recent_transactions,
        'is_admin_user': is_admin_user, # Ajouté au contexte
        'is_agent_group': is_agent_group, # Ajouté au contexte
    }
    return render(request, 'gmycom/dashboard.html', context)

# --- Gestion des clients ---

@login_required
@user_passes_test(is_agent_access, login_url='login')
def client_list(request):
    """
    Affiche la liste de tous les clients avec pagination et recherche/filtrage.
    """
    clients_queryset = Client.objects.all().order_by('nom', 'prenom')

    # Pre-fetch the 'PHOTO_ID' document for each client
    # This avoids N+1 queries when accessing client.photo_document in the template loop
    clients_queryset = clients_queryset.prefetch_related(
        Prefetch('documents', 
                 queryset=ClientDocument.objects.filter(type_document='PHOTO_ID'), 
                 to_attr='photo_document')
    )

    # Filtering logic
    query = request.GET.get('q')
    profession = request.GET.get('profession')
    date_start = request.GET.get('date_start')
    date_end = request.GET.get('date_end')

    if query:
        clients_queryset = clients_queryset.filter(
            Q(nom__icontains=query) |
            Q(prenom__icontains=query) |
            Q(telephone__icontains=query) |
            Q(email__icontains=query) |
            Q(adresse__icontains=query) |
            Q(profession__icontains=query)
        )

    if profession:
        clients_queryset = clients_queryset.filter(profession=profession)

    if date_start:
        try:
            start_date_obj = date.fromisoformat(date_start)
            clients_queryset = clients_queryset.filter(date_inscription__gte=start_date_obj)
        except ValueError:
            messages.error(request, "Format de date de début invalide.")

    if date_end:
        try:
            end_date_obj = date.fromisoformat(date_end)
            clients_queryset = clients_queryset.filter(date_inscription__lte=end_date_obj)
        except ValueError:
            messages.error(request, "Format de date de fin invalide.")

    # Get unique professions for the filter dropdown
    # Use distinct() to avoid duplicates, order_by() is needed before distinct() when using specific fields
    professions = Client.objects.order_by('profession').values_list('profession', flat=True).distinct()


    # Pagination
    paginator = Paginator(clients_queryset, 10) # 10 clients par page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'page_obj': page_obj,  # 'page_obj' contains the paginated clients and pagination info
        'clients': page_obj.object_list, # 'clients' is now the list of client objects for the current page
        'query': query, # Pass the current search query back to the template
        'professions': professions, # Pass unique professions for the filter dropdown
    }
    return render(request, 'gmycom/client_list.html', context)

@login_required
@user_passes_test(is_agent_access, login_url='login')
def client_detail(request, pk):
    """
    Affiche les détails d'un client, ses comptes, crédits et historique de transactions,
    y compris les documents associés avec prévisualisation.
    """
    # Précharge les documents de type 'PHOTO_ID' spécifiquement pour la photo de profil principale.
    # 'documents' est le related_name défini dans votre modèle ClientDocument pour la ForeignKey vers Client.
    photo_id_docs_prefetch = Prefetch(
        'documents',
        queryset=ClientDocument.objects.filter(type_document='PHOTO_ID'),
        to_attr='photo_document' # Le résultat sera stocké dans client.photo_document
    )

    # Précharge TOUS les documents liés au client pour la section "Documents Associés".
    # Il est important de précharger tous les documents dans un attribut distinct
    # car la section "Documents Associés" parcourt tous les documents, pas seulement la photo d'identité.
    all_client_docs_prefetch = Prefetch(
        'documents',
        queryset=ClientDocument.objects.all().order_by('date_telechargement'), # Tri par date par exemple
        to_attr='all_client_documents' # Le résultat sera stocké dans client.all_client_documents
    )

    client = get_object_or_404(
        Client.objects.prefetch_related(photo_id_docs_prefetch, all_client_docs_prefetch),
        pk=pk
    )

    # Comptes, crédits et historique de transactions du client
    comptes = client.comptes.all()
    credits = client.credits.all()
    
    # Historique des transactions du client (tous comptes confondus)
    client_transactions = HistoriqueTransaction.objects.filter(
        Q(compte__client=client) | 
        Q(credit__client=client) | 
        Q(remboursement__credit__client=client)
    ).order_by('-date_operation')[:10]

    # Préparation des variables de contexte pour le rôle de l'utilisateur
    is_admin_user = request.user.is_superuser
    is_agent_group = request.user.groups.filter(name='Agents').exists()

    context = {
        'client': client,
        'comptes': comptes,
        'credits': credits,
        'client_transactions': client_transactions,
        'is_admin_user': is_admin_user, # Ajouté au contexte
        'is_agent_group': is_agent_group, # Ajouté au contexte
    }
    return render(request, 'gmycom/client_detail.html', context)


def client_pdf_view(request, pk):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=2.5*cm, bottomMargin=1.5*cm)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CustomHeading1', parent=styles['h1'], fontSize=20, leading=24, spaceAfter=12, alignment=TA_CENTER, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='CustomHeading2', parent=styles['h2'], fontSize=14, leading=16, spaceBefore=12, spaceAfter=8, fontName='Helvetica-Bold', textColor=colors.darkblue))
    styles.add(ParagraphStyle(name='CustomBodyText', parent=styles['Normal'], fontSize=10, leading=14))
    styles.add(ParagraphStyle(name='CustomBodyTextBold', parent=styles['Normal'], fontSize=10, leading=14, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='SmallText', parent=styles['Normal'], fontSize=8, leading=10, textColor=colors.gray))
    styles.add(ParagraphStyle(name='ErrorText', parent=styles['Normal'], fontSize=9, leading=12, textColor=colors.red))

    elements = []

    client = get_object_or_404(Client.objects.prefetch_related('documents'), pk=pk)

    elements.append(Paragraph("FICHE CLIENT", styles['CustomHeading1']))
    elements.append(Spacer(1, 0.5 * cm))
    elements.append(Paragraph(f"{client.prenom.upper()} {client.nom.upper()}", styles['CustomHeading1']))
    elements.append(Spacer(1, 1 * cm))

    photo_doc = client.documents.filter(type_document='PHOTO_ID').first()
    photo_displayed = False

    if photo_doc and photo_doc.fichier:
        try:
            image_path = photo_doc.fichier.path 
            if os.path.exists(image_path):
                img = Image(image_path)
                img_width = 4 * cm
                img_height = img.drawHeight * img_width / img.drawWidth
                max_img_height = 5 * cm
                if img_height > max_img_height:
                    img_height = max_img_height
                    img_width = img.drawWidth * img_height / img.drawHeight
                img.drawWidth = img_width
                img.drawHeight = img_height
                img.hAlign = 'CENTER'
                elements.append(img)
                elements.append(Spacer(1, 0.5 * cm))
                photo_displayed = True
            else:
                elements.append(Paragraph(f"<font color='red'><i>(Image non trouvée : {os.path.basename(image_path)})</i></font>", styles['ErrorText']))
                elements.append(Spacer(1, 0.5 * cm))
        except Exception as e:
            elements.append(Paragraph(f"<font color='red'><i>(Erreur image : {e})</i></font>", styles['ErrorText']))
            elements.append(Spacer(1, 0.5 * cm))

    if not photo_displayed:
        elements.append(Paragraph("<i>(Photo d'identité non disponible)</i>", styles['SmallText']))
        elements.append(Spacer(1, 0.5 * cm))

    elements.append(Paragraph("<b>INFORMATIONS PERSONNELLES</b>", styles['CustomHeading2']))
    personal_data = [
        ["Nom Complet:", f"{client.prenom} {client.nom}"],
        ["Date de Naissance:", client.date_naissance.strftime('%d/%m/%Y') if client.date_naissance else 'N/A'],
        ["Lieu de Naissance:", client.lieu_naissance or 'N/A'],
        ["Nationalité:", client.nationalite or 'N/A'],
        ["Sexe:", client.get_sexe_display() or 'N/A'],
        ["Situation Matrimoniale:", client.get_situation_matrimoniale_display() or 'N/A'],
        ["Personnes à Charge:", str(client.nombre_personnes_charge) if client.nombre_personnes_charge is not None else 'N/A'],
    ]
    table_style = TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ])
    formatted_personal_data = [[Paragraph(label, styles['CustomBodyTextBold']), Paragraph(value, styles['CustomBodyText'])] for label, value in personal_data]
    elements.append(Table(formatted_personal_data, colWidths=[4*cm, 10*cm], style=table_style))
    elements.append(Spacer(1, 0.8 * cm))

    elements.append(Paragraph("<b>COORDONNÉES</b>", styles['CustomHeading2']))
    contact_data = [
        ["Téléphone:", client.telephone or 'N/A'],
        ["Email:", client.email or 'N/A'],
        ["Adresse:", client.adresse or 'N/A'],
        ["Pays de Résidence:", client.adresse_pays or 'N/A'],
    ]
    formatted_contact_data = [[Paragraph(label, styles['CustomBodyTextBold']), Paragraph(value, styles['CustomBodyText'])] for label, value in contact_data]
    elements.append(Table(formatted_contact_data, colWidths=[4*cm, 10*cm], style=table_style))
    elements.append(Spacer(1, 0.8 * cm))

    elements.append(Paragraph("<b>INFORMATIONS PROFESSIONNELLES ET FINANCIÈRES</b>", styles['CustomHeading2']))
    prof_fin_data = [
        ["Profession:", client.profession or 'N/A'],
        ["Secteur d'activité:", client.secteur_activite or 'N/A'],
        ["Revenu Mensuel:", f"{client.revenu_mensuel:,.2f} XOF" if client.revenu_mensuel is not None else 'N/A'],
        ["Fréquence Revenu:", client.get_frequence_revenu_display() or 'N/A'],
        ["Employeur:", client.nom_employeur or 'N/A'],
        ["Ancienneté (mois):", str(client.anciennete_emploi) if client.anciennete_emploi is not None else 'N/A'],
    ]
    formatted_prof_fin_data = [[Paragraph(label, styles['CustomBodyTextBold']), Paragraph(value, styles['CustomBodyText'])] for label, value in prof_fin_data]
    elements.append(Table(formatted_prof_fin_data, colWidths=[6*cm, 10*cm], style=table_style))
    elements.append(Spacer(1, 0.8 * cm))

    elements.append(Paragraph("<b>INFORMATIONS ADMINISTRATIVES</b>", styles['CustomHeading2']))
    admin_data = [
        ["Date de Création:", client.date_creation.strftime('%d/%m/%Y %H:%M')],
        ["Dernière Modification:", client.date_modification.strftime('%d/%m/%Y %H:%M')],
        ["Agent Responsable:", client.agent.get_full_name() if client.agent else 'Non assigné'],
        ["Statut Actif:", 'Oui' if client.is_active else 'Non'],
    ]
    formatted_admin_data = [[Paragraph(label, styles['CustomBodyTextBold']), Paragraph(value, styles['CustomBodyText'])] for label, value in admin_data]
    elements.append(Table(formatted_admin_data, colWidths=[5*cm, 10*cm], style=table_style))
    elements.append(Spacer(1, 0.8 * cm))

    try:
        doc.build(elements)
    except Exception as e:
        messages.error(request, f"Une erreur est survenue lors de la construction du PDF : {e}")
        return redirect('client_detail', pk=pk)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    filename = f"fiche_client_{client.nom.replace(' ', '_').lower()}_{client.prenom.replace(' ', '_').lower()}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@login_required
@user_passes_test(is_agent_access, login_url='login')
def client_create(request):

    is_admin_user = request.user.is_superuser
    is_agent_group = request.user.groups.filter(name='Agents').exists()

    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        formset = ClientDocumentFormSet(request.POST, request.FILES, prefix='documents') # Ajout du formset

        if form.is_valid() and formset.is_valid():
            try:
                with db_transaction.atomic(): # Utilisation d'une transaction atomique
                    client = form.save(commit=False)
                    client.agent = request.user
                    client.save()                    
                    formset.instance = client # Associer le formset à l'instance client
                    formset.save() # Sauvegarder les documents
                    messages.success(request, "Client créé avec succès et compte épargne ouvert automatiquement !")
                    return JsonResponse({'success': True, 'redirect_url': ''}) # Redirection gérée par JS
            except ValueError as e:
                return JsonResponse({'success': False, 'message': f"Erreur lors de la création du client : {e}"}, status=400)
            except Exception as e:
                return JsonResponse({'success': False, 'message': f"Une erreur inattendue est survenue : {e}"}, status=500)
        else:
            # Collecte de toutes les erreurs pour les renvoyer au JavaScript
            errors = form.errors.get_json_data()
            formset_errors = []
            for i, doc_form in enumerate(formset):
                if doc_form.errors:
                    # Ajoute les erreurs du formset avec leur index
                    formset_errors.append({f'documents-{i}': doc_form.errors.get_json_data()})

            all_errors = {'main_form': errors, 'formset_forms': formset_errors}
            return JsonResponse({'success': False, 'message': 'Erreurs de validation. Veuillez vérifier les champs.', 'errors': all_errors}, status=400)

    else:
        form = ClientForm()
        formset = ClientDocumentFormSet(prefix='documents') # Instancier pour la requête GET

    context = {
        'form': form,
        'formset': formset, # Passer le formset au template
        'title': "Ajouter un client",
        'is_admin_user': is_admin_user, # Ajouté au contexte
        'is_agent_group': is_agent_group, # Ajouté au contexte
    }

    return render(request, 'gmycom/client_form.html', context)



@login_required
@user_passes_test(is_agent_access, login_url='login')
def client_update(request, pk):
    """
    Met à jour les informations d'un client existant.
    """
    client = get_object_or_404(Client, pk=pk)
    is_admin_user = request.user.is_superuser
    is_agent_group = request.user.groups.filter(name='Agents').exists()

    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=client)
        formset = ClientDocumentFormSet(request.POST, request.FILES, instance=client, prefix='documents') # Ajout du formset

        if form.is_valid() and formset.is_valid():
            try:
                with db_transaction.atomic():
                    form.save()
                    formset.save() # Sauvegarder les documents
                
                messages.success(request, "Client mis à jour avec succès !")
                return JsonResponse({'success': True, 'redirect_url': f'/clients/{client.pk}/'}) # Redirection gérée par JS
            except Exception as e:
                return JsonResponse({'success': False, 'message': f"Erreur lors de la mise à jour du client : {e}"}, status=400)
        else:
            errors = form.errors.as_dict()
            formset_errors = []
            for i, doc_form in enumerate(formset):
                if doc_form.errors:
                    formset_errors.append({f'documents-{i}': doc_form.errors.as_dict()})
            all_errors = {'main_form': errors, 'formset_forms': formset_errors}
            return JsonResponse({'success': False, 'message': 'Erreurs de validation. Veuillez vérifier les champs.', 'errors': all_errors}, status=400)
    else:
        form = ClientForm(instance=client)
        formset = ClientDocumentFormSet(instance=client, prefix='documents') # Instancier pour la requête GET
    
    context = {
        'form': form, 
        'formset': formset, # Passer le formset au template
        'title': f"Modifier {client.prenom} {client.nom}",
        'is_admin_user': is_admin_user, 
        'is_agent_group': is_agent_group,
        'client': client, # Passer l'objet client pour les IDs du formset (ex: value="{{ client.pk }}")
    }
    return render(request, 'gmycom/client_form.html', context)



@login_required
@require_POST
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if not request.user.is_superuser and client.agent != request.user:
        messages.error(request, "Vous n’avez pas l’autorisation de supprimer ce client.")
        return redirect('client_list')
    client.delete()
    messages.success(request, f"Le client {client.nom} {client.prenom} a été supprimé avec succès.")
    return redirect('client_list')


# --- Gestion des comptes ---

@login_required
@user_passes_test(is_agent_access, login_url='login')
def compte_list(request):
    """
    Affiche la liste de tous les comptes avec pagination, recherche et totaux de transactions.
    """
    query = request.GET.get('q')
    type_filter = request.GET.get('type')
    statut_filter = request.GET.get('statut')

    # Commencez par tous les comptes et préchargez le client pour éviter les requêtes N+1
    # Annotez avec les sommes des dépôts et retraits.
    # 'historiquetransaction_set' est le related_name par défaut de HistoriqueTransaction vers Compte.
    comptes_queryset = Compte.objects.select_related('client').annotate(
        total_depots=Sum(
            'historique_compte__montant',
            filter=Q(historique_compte__type_operation='DEPOT')
        ),
        total_retraits=Sum(
            'historique_compte__montant',
            filter=Q(historique_compte__type_operation='RETRAIT')
        )
    )

    # Appliquez les filtres de recherche et de sélection
    if query:
        comptes_queryset = comptes_queryset.filter(
            Q(numero_compte__icontains=query) |
            Q(client__nom__icontains=query) |
            Q(client__prenom__icontains=query)
        )

    if type_filter:
        comptes_queryset = comptes_queryset.filter(type_compte=type_filter)

    if statut_filter:
        if statut_filter == 'active':
            comptes_queryset = comptes_queryset.filter(is_active=True)
        elif statut_filter == 'inactive':
            comptes_queryset = comptes_queryset.filter(is_active=False)
        elif statut_filter == 'positive':
            comptes_queryset = comptes_queryset.filter(solde__gt=0)
        elif statut_filter == 'negative':
            comptes_queryset = comptes_queryset.filter(solde__lt=0)

    # Ordre par défaut
    comptes_queryset = comptes_queryset.order_by('numero_compte')

    # Pagination
    paginator = Paginator(comptes_queryset, 10) # 10 comptes par page
    page = request.GET.get('page')
    try:
        comptes = paginator.page(page)
    except PageNotAnInteger:
        comptes = paginator.page(1)
    except EmptyPage:
        # Si la page demandée est en dehors de la plage, délivre la dernière page de résultats
        comptes = paginator.page(paginator.num_pages)

    # Calcule le solde total des comptes affichés sur la page actuelle (pour la petite statistique en haut)
    solde_total_page = sum(compte.solde for compte in comptes) if comptes else Decimal('0.00')

    # Préparation des variables de contexte pour le rôle de l'utilisateur
    is_admin_user = request.user.is_superuser
    is_agent_group = request.user.groups.filter(name='Agents').exists()

    context = {
        'comptes': comptes, # 'comptes' est maintenant l'objet Page, qui est itérable
        'solde_total': solde_total_page, 
        'query': query, # Passe la variable de recherche pour maintenir la valeur dans le champ
        'type_filter': type_filter, # Passe les variables de filtre pour maintenir les sélections
        'statut_filter': statut_filter,
        'is_paginated': comptes.has_other_pages, # Utilise has_other_pages de l'objet Page
        'page_obj': comptes, # Passe l'objet Page directement pour les liens de pagination
        'is_admin_user': is_admin_user, 
        'is_agent_group': is_agent_group,
    }
    return render(request, 'gmycom/compte_list.html', context)


@login_required
@user_passes_test(is_agent_access, login_url='login')
def compte_detail(request, pk):
    """
    Affiche les détails d'un compte et son historique de transactions.
    """
    compte = get_object_or_404(Compte, pk=pk)
    # Filtrer les transactions associées directement à ce compte
    transactions = HistoriqueTransaction.objects.filter(compte=compte).order_by('-date_operation')

    paginator = Paginator(transactions, 15) # 15 transactions par page
    page = request.GET.get('page')
    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)

    # Préparation des variables de contexte pour le rôle de l'utilisateur
    is_admin_user = request.user.is_superuser
    is_agent_group = request.user.groups.filter(name='Agents').exists()

    context = {
        'compte': compte,
        'transactions': transactions,
        'is_admin_user': is_admin_user, # Ajouté au contexte
        'is_agent_group': is_agent_group, # Ajouté au contexte
    }
    return render(request, 'gmycom/compte_detail.html', context)

@login_required 
@user_passes_test(is_agent_access, login_url='login')
def search_clients_ajax(request):
    query = request.GET.get('q', '')
    clients = []
    if query:
        # Recherche par nom, prénom, email ou téléphone
        client_results = Client.objects.filter(
            Q(nom__icontains=query) |
            Q(prenom__icontains=query) |
            Q(email__icontains=query) | # <-- CORRIGÉ ICI: UTILISE L'EMAIL
            Q(telephone__icontains=query)
        ).distinct()[:10] # Limiter les résultats pour la performance

        for client in client_results:
            # Afficher l'email ou la CNI si disponible, pour une meilleure identification
            identifier = client.email or client.telephone or 'N/A'
            clients.append({
                'id': client.pk,
                'text': f"{client.nom} {client.prenom} (email: {identifier})" # Adaptez le texte affiché si nécessaire
            })
    return JsonResponse(clients, safe=False)


@login_required
@user_passes_test(is_agent_access, login_url='login')
def compte_create(request, client_id=None):
    """
    Ouvre un nouveau compte pour un client. Peut être pré-rempli avec client_id.
    """
    client_instance = None
    initial_data = {}

    if client_id:
        client_instance = get_object_or_404(Client, pk=client_id)
        # Ne pré-remplissez pas 'client' directement dans initial_data pour le form Django ici.
        # Le template gérera l'affichage et le champ caché.
        pass

    if request.method == 'POST':
        # Le champ 'client' viendra de l'input caché 'client_id_hidden' dans le template.
        # Nous devons le récupérer manuellement ou nous assurer que le formulaire le traite.
        # Puisque le formulaire attend un PK, on va s'assurer de le récupérer correctement.
        selected_client_pk = request.POST.get('client_id_hidden') # Nom de l'input caché dans le template
        
        # Créer une copie de POST data pour pouvoir la modifier
        post_data = request.POST.copy()
        if selected_client_pk:
            post_data['client'] = selected_client_pk # Force la valeur du client dans les données POST
        
        form = CompteForm(post_data) # Passer les données POST modifiées au formulaire

        if form.is_valid():
            compte = form.save(commit=False)
            compte.opened_by = request.user
            try:
                compte.save()
                messages.success(request, f"Compte {compte.numero_compte} créé avec succès pour {compte.client.nom} {compte.client.prenom}!")
                return redirect('compte_list', pk=compte.pk)
            except ValueError as e:
                messages.error(request, f"Erreur lors de la création du compte : {e}")
            except Exception as e:
                messages.error(request, f"Une erreur inattendue est survenue : {e}")
        else:
            messages.error(request, "Erreur lors de la création du compte. Veuillez vérifier les champs.")
            # Si le formulaire n'est pas valide et que le client était pré-sélectionné,
            # nous devons recréer client_instance pour que le template puisse l'afficher.
            if client_id:
                client_instance = get_object_or_404(Client, pk=client_id)
            elif selected_client_pk: # Si un client a été sélectionné via AJAX mais le formulaire échoue
                 try:
                    client_instance = Client.objects.get(pk=selected_client_pk)
                 except Client.DoesNotExist:
                     client_instance = None # Client non trouvé, réinitialiser

    else: # GET request
        form = CompteForm()
        # Initialiser les valeurs si un client_id est passé dans l'URL
        if client_id:
            client_instance = get_object_or_404(Client, pk=client_id)
            # Ne désactivez pas le champ du formulaire de Django, car nous allons le cacher.
            # L'ID sera envoyé via un input hidden.

    context = {
        'form': form, 
        'title': "Ouvrir un nouveau compte",
        'client_instance': client_instance, # Passe l'instance du client au template si disponible
        'is_admin_user': request.user.is_superuser, 
        'is_agent_group': request.user.groups.filter(name='Agents').exists(),
    }
    return render(request, 'gmycom/compte_form.html', context)

@login_required
@require_POST
def compte_delete(request, pk):
    """
    Supprime un compte spécifié par son identifiant (pk).
    Cette action est irréversible et réservée aux administrateurs (superutilisateurs).
    """
    compte = get_object_or_404(Compte, pk=pk)
    compte_numero = compte.numero_compte # Capture le numéro de compte avant la suppression pour les messages

    if request.method == 'POST':
        try:
            with db_transaction.atomic(): # Utilise une transaction atomique pour garantir l'intégrité
                compte.delete()
                messages.success(request, f"Le compte '{compte_numero}' a été supprimé avec succès.")
            return redirect('compte_list') # Redirige vers la liste des comptes après suppression
        except Exception as e:
            # Gère les erreurs potentielles lors de la suppression
            messages.error(request, f"Une erreur est survenue lors de la suppression du compte '{compte_numero}' : {e}")
            return redirect('compte_list') # En cas d'erreur, redirige également vers la liste
    messages.warning(request, f"Veuillez confirmer la suppression du compte '{compte_numero}' via le formulaire de confirmation. Accès direct non autorisé.")
    return redirect('compte_list')


# --- Gestion des mouvements (dépôt/retrait/virement) ---


from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.db.models import Q
from django.http import JsonResponse
from .models import Compte

@login_required
@require_GET
def search_comptes_ajax(request):
    query = request.GET.get('q', '')
    compte_id = request.GET.get('id', '')
    comptes_data = []

    if compte_id:
        try:
            compte = Compte.objects.select_related('client').get(pk=compte_id)
            if compte.client:
                comptes_data.append({
                    'id': compte.pk,
                    'client_id': compte.client.pk,  # ✅ ID du client ajouté ici
                    'numero_compte': compte.numero_compte,
                    'client_nom': compte.client.nom,
                    'client_prenom': compte.client.prenom,
                    'type_compte_display': compte.get_type_compte_display(),
                    'solde': str(compte.solde),
                    'affichage': f"{compte.numero_compte} - {compte.client.nom} {compte.client.prenom} ({compte.get_type_compte_display()}) - {compte.client.email}"
                })
        except Compte.DoesNotExist:
            pass

    elif query and len(query) >= 2:
        comptes = Compte.objects.select_related('client').filter(
            is_active=True
        ).filter(
            Q(numero_compte__icontains=query) |
            Q(client__nom__icontains=query) |
            Q(client__prenom__icontains=query) |
            Q(client__email__icontains=query)
        )[:20]

        for compte in comptes:
            if compte.client:
                comptes_data.append({
                    'id': compte.pk,
                    'client_id': compte.client.pk,  # ✅ ID du client ajouté ici
                    'numero_compte': compte.numero_compte,
                    'client_nom': compte.client.nom,
                    'client_prenom': compte.client.prenom,
                    'client_email': compte.client.email,
                    'type_compte_display': compte.get_type_compte_display(),
                    'solde': str(compte.solde),
                    'affichage': f"{compte.numero_compte} - {compte.client.nom} {compte.client.prenom} ({compte.get_type_compte_display()}) - {compte.client.email}"
                })

    return JsonResponse(comptes_data, safe=False)




@login_required
@user_passes_test(is_agent_access, login_url='login')
def mouvement_create(request, compte_id=None):
    """
    Enregistre un dépôt, un retrait ou un virement sur un compte.
    """
    initial_data = {}
    if compte_id:
        compte = get_object_or_404(Compte, pk=compte_id)
        initial_data['compte'] = compte.pk

    is_admin_user = request.user.is_superuser
    is_agent_group = request.user.groups.filter(name='Agents').exists()

    if request.method == 'POST':
        form = MouvementForm(request.POST, request.FILES, initial=initial_data)
        if compte_id:
            form.fields['compte'].widget.attrs.pop('disabled', None)

        if form.is_valid():
            mouvement_obj = form.save(commit=False)
            mouvement_obj.agent = request.user
            try:
                mouvement_obj.save()

                # ✅ Si c'est une requête AJAX → réponse JSON
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        "success": True,
                        "message": f"Mouvement de {mouvement_obj.montant} XOF ({mouvement_obj.get_type_mouvement_display()}) enregistré avec succès!",
                        "redirect_url": reverse('transaction_history_list')
                    })

                # Sinon, redirection classique
                messages.success(request, f"Mouvement de {mouvement_obj.montant} XOF ({mouvement_obj.get_type_mouvement_display()}) enregistré avec succès!")
                return redirect('transaction_history_list')

            except ValueError as e:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        "success": False,
                        "message": f"Erreur lors de l'opération : {e}"
                    }, status=400)
                messages.error(request, f"Erreur lors de l'opération : {e}")
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    "success": False,
                    "message": "Erreur de validation",
                    "errors": form.errors
                }, status=400)
            messages.error(request, "Erreur lors de l'opération. Veuillez vérifier les champs.")
    else:
        form = MouvementForm(initial=initial_data)
        if compte_id:
            form.fields['compte'].widget.attrs['disabled'] = True
            form.fields['compte'].queryset = Compte.objects.filter(pk=compte_id)

    context = {
        'form': form,
        'title': "Enregistrer un mouvement",
        'is_admin_user': is_admin_user,
        'is_agent_group': is_agent_group,
    }
    return render(request, 'gmycom/mouvement_form.html', context)



@login_required
@user_passes_test(is_agent_access, login_url='login')
def transaction_history_list(request):
    """
    Affiche la liste complète de l'historique des transactions avec pagination et filtres.
    """
    transactions_queryset = HistoriqueTransaction.objects.select_related(
        'compte', 'compte__client', 'credit', 'credit__client', 'remboursement', 'remboursement__credit__client', 'agent'
    ).order_by('-date_operation')

    # Filtering logic
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    transaction_type = request.GET.get('type')
    client_name = request.GET.get('client_name')
    min_amount_str = request.GET.get('min_amount')
    max_amount_str = request.GET.get('max_amount')

    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            transactions_queryset = transactions_queryset.filter(date_operation__gte=start_date)
        except ValueError:
            messages.error(request, "Format de date de début invalide.")

    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1) # Include full end date
            transactions_queryset = transactions_queryset.filter(date_operation__lt=end_date)
        except ValueError:
            messages.error(request, "Format de date de fin invalide.")

    if transaction_type:
        if transaction_type != '': # 'all' case is handled by not applying filter
            transactions_queryset = transactions_queryset.filter(type_operation=transaction_type)

    if client_name:
        transactions_queryset = transactions_queryset.filter(
            Q(compte__client__nom__icontains=client_name) |
            Q(compte__client__prenom__icontains=client_name) |
            Q(credit__client__nom__icontains=client_name) |
            Q(credit__client__prenom__icontains=client_name) |
            Q(remboursement__credit__client__nom__icontains=client_name) |
            Q(remboursement__credit__client__prenom__icontains=client_name)
        )

    if min_amount_str:
        try:
            min_amount = Decimal(min_amount_str)
            transactions_queryset = transactions_queryset.filter(montant__gte=min_amount)
        except InvalidOperation:
            messages.error(request, "Montant minimum invalide.")

    if max_amount_str:
        try:
            max_amount = Decimal(max_amount_str)
            transactions_queryset = transactions_queryset.filter(montant__lte=max_amount)
        except InvalidOperation:
            messages.error(request, "Montant maximum invalide.")

    # Calculate Summary Statistics for *all* filtered transactions (not just the current page)
    total_deposits = transactions_queryset.filter(
        Q(type_operation='DEPOT') | Q(type_operation='VIREMENT_RECU')
    ).aggregate(total=Coalesce(Sum('montant'), Decimal('0.00')))['total']

    total_withdrawals = transactions_queryset.filter(
        Q(type_operation='RETRAIT') | Q(type_operation='VIREMENT')
    ).aggregate(total=Coalesce(Sum('montant'), Decimal('0.00')))['total']
    
    total_transactions_count = transactions_queryset.count()

    net_balance = total_deposits - total_withdrawals

    # Pagination
    paginator = Paginator(transactions_queryset, 20) # 20 transactions per page
    page = request.GET.get('page')
    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)

    # Prepare data for JavaScript receipt modal
    transactions_data_for_js = []
    for tx in transactions.object_list: # Iterate over transactions for the current page
        client_full_name = 'N/A'
        if tx.compte and tx.compte.client:
            client_full_name = f"{tx.compte.client.prenom} {tx.compte.client.nom}"
        elif tx.credit and tx.credit.client:
            client_full_name = f"{tx.credit.client.prenom} {tx.credit.client.nom}"
        elif tx.remboursement and tx.remboursement.credit and tx.remboursement.credit.client:
            client_full_name = f"{tx.remboursement.credit.client.prenom} {tx.remboursement.credit.client.nom}"

        transactions_data_for_js.append({
            'id': tx.id,
            'type_operation': tx.type_operation,
            'type_operation_display': tx.get_type_operation_display(),
            'montant': str(tx.montant), # Convert Decimal to string for JSON serialization
            'date_operation': tx.date_operation.isoformat(),
            'description': tx.description,
            'solde_avant': str(tx.solde_avant) if tx.solde_avant is not None else None,
            'solde_apres': str(tx.solde_apres) if tx.solde_apres is not None else None,
            'client_full_name': client_full_name,
            'compte_numero': tx.compte.numero_compte if tx.compte else 'N/A',
            'agent_username': tx.agent.username if tx.agent else 'Système', # Add agent who processed
        })

    is_admin_user = request.user.is_superuser
    is_agent_group = request.user.groups.filter(name='Agents').exists()

    context = {
        'transactions': transactions, # Paginator object
        'total_transactions': total_transactions_count,
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
        'net_balance': net_balance,
        'transaction_types': HistoriqueTransaction.TYPE_OPERATION_CHOICES, # Pass choices for filter dropdown
        'transactions_json': json.dumps(transactions_data_for_js), # JSON data for JS
        'is_admin_user': is_admin_user, 
        'is_agent_group': is_agent_group,
    }
    return render(request, 'gmycom/transaction_history_list.html', context)

# --- Gestion des crédits ---

@login_required
@user_passes_test(is_agent_access, login_url='login')
def credit_list(request):
    """
    Affiche la liste de tous les crédits avec filtres.
    """
    credits = Credit.objects.select_related('client', 'compte').all()
    status_filter = request.GET.get('status')
    client_filter = request.GET.get('client')

    if status_filter:
        credits = credits.filter(status=status_filter)
    if client_filter:
        credits = credits.filter(client__id=client_filter)

    paginator = Paginator(credits, 10)
    page = request.GET.get('page')
    try:
        credits = paginator.page(page)
    except PageNotAnInteger:
        credits = paginator.page(1)
    except EmptyPage:
        credits = paginator.page(paginator.num_pages)

    # Préparation des variables de contexte pour le rôle de l'utilisateur
    is_admin_user = request.user.is_superuser
    is_agent_group = request.user.groups.filter(name='Agents').exists()

    context = {
        'credits': credits,
        'credit_statuses': Credit.CREDIT_STATUSES,
        'clients': Client.objects.all(),
        'selected_status': status_filter,
        'selected_client': client_filter,
        'is_admin_user': is_admin_user, # Ajouté au contexte
        'is_agent_group': is_agent_group, # Ajouté au contexte
    }
    return render(request, 'gmycom/credit_list.html', context)

@login_required
@user_passes_test(is_agent_access, login_url='login')
def credit_detail(request, pk):
    """
    Affiche les détails d'un crédit et son historique de remboursements.
    """
    credit = get_object_or_404(Credit, pk=pk)
    remboursements = credit.remboursements.all().order_by('-date_remboursement')

    # Préparation des variables de contexte pour le rôle de l'utilisateur
    is_admin_user = request.user.is_superuser
    is_agent_group = request.user.groups.filter(name='Agents').exists()

    context = {
        'credit': credit,
        'remboursements': remboursements,
        'is_admin_user': is_admin_user, # Ajouté au contexte
        'is_agent_group': is_agent_group, # Ajouté au contexte
    }
    return render(request, 'gmycom/credit_detail.html', context)

@login_required
@user_passes_test(is_agent_access, login_url='login')
def credit_create(request, client_id=None):
    """
    Enregistre un nouveau crédit.
    """
    initial_data = {}
    if client_id:
        client = get_object_or_404(Client, pk=client_id)
        initial_data['client'] = client.pk
        initial_data['compte_queryset'] = Compte.objects.filter(client=client)

    is_admin_user = request.user.is_superuser
    is_agent_group = request.user.groups.filter(name='Agents').exists()

    if request.method == 'POST':
        form = CreditForm(request.POST)
        
        # Injection dynamique des querysets pour la validation
        if client_id:
            form.fields['client'].queryset = Client.objects.filter(pk=client_id)
            form.fields['compte'].queryset = Compte.objects.filter(client=client)

        # Important : enlever tout champ désactivé dans le widget
        form.fields['client'].widget.attrs.pop('disabled', None)

        if form.is_valid():
            credit = form.save(commit=False)
            credit.granted_by = request.user
            try:
                credit.save()
                messages.success(request, f"Crédit {credit.numero_credit} enregistré avec succès !")
                return redirect('credit_list')
            except ValueError as e:
                messages.error(request, f"Erreur lors de l'enregistrement du crédit : {e}")
        else:
            print("Form errors:", form.errors.as_json())  # Debug console
            messages.error(request, "Erreur lors de l'enregistrement du crédit. Veuillez vérifier les champs.")
    else:
        form = CreditForm(initial=initial_data)
        if client_id:
            form.fields['client'].widget.attrs['disabled'] = True
            form.fields['client'].queryset = Client.objects.filter(pk=client_id)
            form.fields['compte'].queryset = Compte.objects.filter(client=client)

    context = {
        'form': form,
        'title': "Enregistrer un nouveau crédit",
        'is_admin_user': is_admin_user,
        'is_agent_group': is_agent_group,
    }
    return render(request, 'gmycom/credit_form.html', context)



def get_compte_details(request):
    """
    Retourne les détails d'un compte spécifique au format JSON pour les requêtes AJAX.
    Utilisé par le JavaScript du formulaire de crédit.
    """
    account_id = request.GET.get('account_id')
    if not account_id:
        return JsonResponse({'success': False, 'message': 'L\'ID du compte est requis.'}, status=400)

    try:
        compte = get_object_or_404(Compte, pk=account_id)
        # Assurez-vous que votre modèle Client a une propriété 'full_name'
        # Sinon, utilisez par exemple: f"{compte.client.prenom} {compte.client.nom}"
        affichage = f"{compte.client.full_name} ({compte.numero_compte})"

        data = {
            'success': True,
            'id': compte.pk,
            'numero_compte': compte.numero_compte,
            'client_id': compte.client.pk,
            'client_full_name': compte.client.full_name, # Peut-être utile pour l'affichage initial
            'affichage': affichage, # La chaîne formatée pour le champ de recherche
        }
        return JsonResponse(data)
    except Compte.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Compte non trouvé.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Erreur interne: {str(e)}"}, status=500)


# --- Gestion des remboursements ---

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .forms import RemboursementForm
from .models import Credit, Remboursement

@login_required
@user_passes_test(is_agent_access, login_url='login')
def remboursement_create(request, credit_id=None):
    def request_is_ajax(req):
        return req.headers.get('x-requested-with') == 'XMLHttpRequest'

    initial_data = {}
    credit = None
    if credit_id:
        credit = get_object_or_404(Credit, pk=credit_id)
        initial_data['credit'] = credit.pk
        initial_data['montant'] = credit.remaining_total_due

    is_admin_user = request.user.is_superuser
    is_agent_group = request.user.groups.filter(name='Agents').exists()

    if request.method == 'POST':
        form = RemboursementForm(request.POST)
        print(">>> CREDIT SUBMITTED:", request.POST.get('credit'))
        if credit_id:
            form.fields['credit'].queryset = Credit.objects.filter(pk=credit_id)
            form.fields['credit'].widget.attrs['readonly'] = True  # Ne pas utiliser disabled !

        if form.is_valid():
            remboursement = form.save(commit=False)
            remboursement.agent = request.user
            try:
                remboursement.save()
                success_message = f"Remboursement de {remboursement.montant} XOF enregistré pour le crédit {remboursement.credit.numero_credit}."
                if request_is_ajax(request):
                    return JsonResponse({'success': True, 'message': success_message})
                messages.success(request, success_message)
                return redirect('transaction_history_list')
            except Exception as e:
                error_message = f"Erreur lors de l'enregistrement : {str(e)}"
                if request_is_ajax(request):
                    return JsonResponse({'success': False, 'message': error_message})
                messages.error(request, error_message)
        else:
            # Ajoutez cette ligne pour voir les erreurs de validation dans votre console de serveur
            print("Formulaire invalide. Erreurs:", form.errors)
            errors = form.errors.get_json_data()
            if request_is_ajax(request):
                return JsonResponse({'success': False, 'message': 'Formulaire invalide', 'errors': errors})
            messages.error(request, "Erreur lors de l'enregistrement du remboursement. Veuillez vérifier les champs.")
    else:
        form = RemboursementForm(initial=initial_data)
        if credit_id:
            form.fields['credit'].queryset = Credit.objects.filter(pk=credit_id)
            form.fields['credit'].widget.attrs['readonly'] = True  # Et ici aussi, readonly au lieu de disabled

    context = {
        'form': form,
        'title': "Enregistrer un remboursement",
        'is_admin_user': is_admin_user,
        'is_agent_group': is_agent_group,
        'credit': credit,
    }
    return render(request, 'gmycom/remboursement_form.html', context)

# --- Rapports simples ---

@login_required
@user_passes_test(is_agent_access, login_url='login')
def situation_report(request):
    """
    Génère un rapport de situation (clients avec solde, crédits en cours, etc.).
    """
    report_type = request.GET.get('type', 'clients_balance')
    data = []
    title = ""

    if report_type == 'clients_balance':
        title = "Rapport : Clients et Solde de leurs comptes"
        clients_with_balance = Client.objects.annotate(
            total_balance=Sum('comptes__solde')
        ).order_by('nom')
        data = clients_with_balance

    elif report_type == 'active_credits':
        title = "Rapport : Crédits en cours"
        active_credits = Credit.objects.filter(status='ACTIVE').select_related('client').order_by('due_date')
        data = active_credits

    elif report_type == 'transactions_history':
        title = "Rapport : Historique des transactions"
        # Vous pouvez ajouter des filtres de date ici si nécessaire
        transactions_history = HistoriqueTransaction.objects.select_related('compte__client').order_by('-date_operation')[:100] # Limiter pour le rapport
        data = transactions_history
    
    elif report_type == 'summary_metrics':
        title = "Rapport : Métriques Résumées"
        total_clients = Client.objects.count()
        total_comptes_open = Compte.objects.filter(is_active=True).count()
        total_balance_all_comptes = Compte.objects.aggregate(Sum('solde'))['solde__sum'] or Decimal('0.00')
        total_credits_granted = Credit.objects.aggregate(Sum('amount_granted'))['amount_granted__sum'] or Decimal('0.00')
        total_credits_repaid = Credit.objects.aggregate(Sum('amount_repaid'))['amount_repaid__sum'] or Decimal('0.00')
        
        data = {
            'total_clients': total_clients,
            'total_comptes_open': total_comptes_open,
            'total_balance_all_comptes': total_balance_all_comptes,
            'total_credits_granted': total_credits_granted,
            'total_credits_repaid': total_credits_repaid,
            'active_credits_count': Credit.objects.filter(status='ACTIVE').count(),
            'repaid_credits_count': Credit.objects.filter(status='REPAID').count(),
        }

    # Préparation des variables de contexte pour le rôle de l'utilisateur
    is_admin_user = request.user.is_superuser
    is_agent_group = request.user.groups.filter(name='Agents').exists()

    context = {
        'report_type': report_type,
        'title': title,
        'data': data,
        'is_admin_user': is_admin_user, # Ajouté au contexte
        'is_agent_group': is_agent_group, # Ajouté au contexte
    }
    return render(request, 'gmycom/situation_report.html', context)


@login_required
@user_passes_test(is_agent_access, login_url='login')
def credit_search_ajax(request):
    query = request.GET.get('q', '')
    credits = []
    if query:
        # Recherche par numéro de crédit, nom, prénom ou email du client
        # Ajout du filtre pour ne rechercher que les crédits "actifs"
        credit_results = Credit.objects.filter(
            Q(numero_credit__icontains=query) |
            Q(client__nom__icontains=query) |
            Q(client__prenom__icontains=query) |
            Q(client__email__icontains=query),
            status='ACTIVE' # Filtrer uniquement les crédits actifs
        ).select_related('client').order_by('numero_credit')[:10] # Limiter à 10 résultats

        for credit in credit_results:
            credits.append({
                'id': credit.pk,
                'numero_credit': credit.numero_credit,
                'client_full_name': f"{credit.client.nom} {credit.client.prenom}",
                'remaining_total_due': float(credit.remaining_total_due), # Convertir Decimal en float pour JSON
            })
    return JsonResponse(credits, safe=False)


def get_credit_details_ajax(request):
    credit_id = request.GET.get('credit_id')
    if not credit_id:
        return JsonResponse({'success': False, 'message': "ID de crédit manquant."}, status=400)

    try:
        credit = get_object_or_404(Credit, pk=credit_id)

        data = {
            'success': True,
            'id': credit.id,
            'numero_credit': credit.numero_credit,
            'client_full_name': f"{credit.client.nom} {credit.client.prenom}",
            'credit_display': f"{credit.numero_credit} - {credit.client.nom} {credit.client.prenom}",
            'montant_credit': float(credit.amount_granted),
            'taux_interet': float(credit.interest_rate),
            'duree_credit': credit.duree_mois,
            'total_rembourse': float(credit.amount_repaid),
            'remaining_total_due': float(credit.remaining_total_due),
            'remaining_principal': float((credit.amount_granted - credit.amount_repaid).quantize(credit.amount_granted)),
            'remaining_interest': float((credit.total_interest_expected - max(0, credit.amount_repaid - credit.amount_granted)).quantize(credit.amount_granted)),
        }
        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


def get_repayments_ajax(request, pk):
    remboursements = Remboursement.objects.filter(credit_id=pk).order_by('-date_remboursement')
    data = {
        'success': True,
        'repayments': [
            {
                'date_remboursement': r.date_remboursement.strftime('%Y-%m-%d'),
                'montant': float(r.montant),
                'methode_paiement': r.methode_paiement,
                'reference': r.reference,
                'notes': r.notes,
            }
            for r in remboursements
        ]
    }
    return JsonResponse(data)


# Vue de confirmation de suppression (réutilisable)
@login_required
@user_passes_test(is_admin_access, login_url='login') # Seuls les superutilisateurs peuvent supprimer
def confirm_delete(request):
    """
    Affiche une page de confirmation avant la suppression.
    """
    # Ce n'est pas une vue autonome, mais un template qui est rendu par d'autres vues de suppression.
    # Le contenu de cette fonction est minimal car la logique de suppression est dans les vues spécifiques.
    pass

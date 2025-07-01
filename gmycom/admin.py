# microfinance_project/gmycom/admin.py

from django.contrib import admin
from .models import (
    Client, ClientDocument, Compte, Mouvement,
    Credit, Remboursement, HistoriqueTransaction
)

# --- Configuration pour ClientDocument (Inline) ---
# Ceci permet de gérer les documents directement depuis la page d'édition d'un client.
class ClientDocumentInline(admin.TabularInline): # Ou admin.StackedInline pour un affichage plus détaillé
    model = ClientDocument
    extra = 0  # Ne pas afficher de formulaires vides par défaut
    fields = ('type_document', 'fichier')
    # readonly_fields = ('date_telechargement',) # Si vous voulez qu'il soit seulement affiché et non modifiable après upload

# --- Configuration pour le modèle Client ---
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'nom', 'prenom', 'telephone', 'email', 
        'nationalite', 'date_creation', 'agent', 'is_active'
    )
    list_filter = (
        'is_active', 'sexe', 'situation_matrimoniale', 
        'profession', 'nationalite', 'agent'
    )
    search_fields = (
        'nom', 'prenom', 'telephone', 'email', 
        'nationalite', 'adresse'
    )
    # Groupement des champs dans le formulaire d'édition
    fieldsets = (
        ('Informations Personnelles', {
            'fields': (
                ('nom', 'prenom'),
                ('date_naissance', 'lieu_naissance'),
                ('nationalite', 'sexe', 'situation_matrimoniale'),
                'nombre_personnes_charge',
            ),
        }),
        ('Coordonnées', {
            'fields': (
                ('telephone', 'email'),
                'adresse', 'adresse_pays',
            ),
        }),
        ('Informations Professionnelles et Financières', {
            'fields': (
                ('profession', 'secteur_activite'),
                ('revenu_mensuel', 'frequence_revenu'),
                ('nom_employeur', 'anciennete_emploi'),
            ),
        }),
        ('Informations Administratives', {
            'fields': (
                'agent', 'is_active',
            ),
            'classes': ('collapse',), # Pour masquer cette section par défaut
        }),
    )
    inlines = [ClientDocumentInline] # Intègre la gestion des documents ici
    date_hierarchy = 'date_creation' # Permet de naviguer par date de création

# --- Configuration pour le modèle Compte ---
@admin.register(Compte)
class CompteAdmin(admin.ModelAdmin):
    list_display = (
        'numero_compte', 'client', 'type_compte', 'solde', 
        'date_ouverture', 'opened_by', 'is_active'
    )
    list_filter = (
        'type_compte', 'is_active', 'opened_by'
    )
    search_fields = (
        'numero_compte', 'client__nom', 'client__prenom', 
        'client__telephone' # Permet de rechercher par les infos du client lié
    )
    raw_id_fields = ('client', 'opened_by') # Pour les champs de clé étrangère, utile si beaucoup d'instances
    readonly_fields = ('date_ouverture',) # La date d'ouverture est auto_now_add

# --- Configuration pour le modèle Mouvement ---
@admin.register(Mouvement)
class MouvementAdmin(admin.ModelAdmin):
    list_display = (
        'compte', 'type_mouvement', 'montant', 'date_mouvement', 
        'compte_destinataire', 'agent'
    )
    list_filter = (
        'type_mouvement', 'agent'
    )
    search_fields = (
        'compte__numero_compte', 'compte__client__nom', 'compte_destinataire__numero_compte'
    )
    raw_id_fields = ('compte', 'compte_destinataire', 'agent')
    readonly_fields = ('date_mouvement',)

# --- Configuration pour le modèle Credit ---
@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = (
        'numero_credit', 'client', 'compte', 'amount_granted', 
        'interest_rate', 'duree_mois', 'status', 'due_date',
        'amount_repaid', 'remaining_total_due', # remaining_total_due est une propriété du modèle
        'granted_by'
    )
    list_filter = (
        'status', 'granted_by', 'due_date'
    )
    search_fields = (
        'numero_credit', 'client__nom', 'client__prenom', 
        'compte__numero_compte'
    )
    raw_id_fields = ('client', 'compte', 'granted_by')
    # total_interest_expected et total_expected_repayment sont calculés dans save(), donc en lecture seule
    # amount_repaid est mis à jour par les remboursements
    readonly_fields = (
        'date_demande', 'total_interest_expected', 
        'total_expected_repayment', 'amount_repaid', 
        'remaining_total_due'
    )

# --- Configuration pour le modèle Remboursement ---
@admin.register(Remboursement)
class RemboursementAdmin(admin.ModelAdmin):
    list_display = (
        'numero_remboursement', 'credit', 'montant', 
        'date_remboursement', 'methode_paiement', 'agent'
    )
    list_filter = (
        'methode_paiement', 'agent'
    )
    search_fields = (
        'numero_remboursement', 'credit__numero_credit', 
        'credit__client__nom'
    )
    raw_id_fields = ('credit', 'agent')
    readonly_fields = ('date_remboursement',)

# --- Configuration pour le modèle HistoriqueTransaction ---
@admin.register(HistoriqueTransaction)
class HistoriqueTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'date_operation', 'compte', 'type_operation', 'montant', 
        'solde_avant', 'solde_apres', 'agent', 'description'
    )
    list_filter = (
        'type_operation', 'agent'
    )
    search_fields = (
        'compte__numero_compte', 'description', 
        'credit__numero_credit', 'remboursement__numero_remboursement',
        'mouvement__compte__numero_compte'
    )
    # Toutes les transactions sont en lecture seule pour maintenir l'intégrité de l'historique
    readonly_fields = (
        'compte', 'credit', 'remboursement', 'mouvement', 
        'type_operation', 'montant', 'date_operation', 
        'solde_avant', 'solde_apres', 'description', 'agent'
    )
    # Empêcher l'ajout ou la suppression directe via l'admin
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False


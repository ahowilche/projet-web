from django import forms
# Correction de l'importation: Assurez-vous que gmycom est dans INSTALLED_APPS
from gmycom.models import Client, Compte, Mouvement, Credit, Remboursement, HistoriqueTransaction, ClientDocument 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from decimal import Decimal
from django.forms import inlineformset_factory 
from django.utils import timezone 


# Formulaire d'authentification (basique)
class AgentLoginForm(AuthenticationForm):
    """
    Formulaire de connexion pour les agents (utilise le modèle User par défaut).
    Utilise Tailwind CSS pour le stylisme des champs.
    """
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
            'placeholder': 'Entrez votre nom d\'utilisateur'
        })
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm',
            'placeholder': 'Entrez votre mot de passe'
        })
    )

    class Meta:
        fields = ['username', 'password']


# Formulaire Client
class ClientForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier un client.
    """
    class Meta:
        model = Client
        fields = [
            'nom', 'prenom', 'date_naissance', 'lieu_naissance', 'nationalite', 'sexe',
            'situation_matrimoniale', 'nombre_personnes_charge',
            'telephone', 'email', 'adresse', 'adresse_pays',
            'profession', 'secteur_activite', 'revenu_mensuel',
            'frequence_revenu', 'nom_employeur', 'anciennete_emploi',
        ]
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'date_naissance': 'Date de naissance',
            'lieu_naissance': 'Lieu de naissance',
            'nationalite': 'Nationalité',
            'sexe': 'Sexe',
            'situation_matrimoniale': 'Situation Matrimoniale',
            'nombre_personnes_charge': 'Nombre de personnes à charge',
            'telephone': 'Téléphone Principal',
            'email': 'Email',
            'adresse': 'Adresse Résidentielle Complète',
            'adresse_pays': 'Pays',
            'profession': 'Profession',
            'secteur_activite': 'Secteur d\'activité',
            'revenu_mensuel': 'Revenu Mensuel',
            'frequence_revenu': 'Fréquence des revenus',
            'nom_employeur': 'Nom de l\'employeur / entreprise',
            'anciennete_emploi': 'Ancienneté (en mois)',
        }
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'sexe': forms.Select(attrs={'class': 'form-select'}),
            'situation_matrimoniale': forms.Select(attrs={'class': 'form-select'}),
            # Correction: profession est un CharField libre, pas un Select
            'profession': forms.TextInput(attrs={'class': 'form-input'}), 
            'nom': forms.TextInput(attrs={'class': 'form-input'}),
            'prenom': forms.TextInput(attrs={'class': 'form-input'}),
            'lieu_naissance': forms.TextInput(attrs={'class': 'form-input'}),
            'nationalite': forms.TextInput(attrs={'class': 'form-input'}),
            'nombre_personnes_charge': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'telephone': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'adresse': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'adresse_pays': forms.TextInput(attrs={'class': 'form-input'}),
            'secteur_activite': forms.TextInput(attrs={'class': 'form-input'}),
            'revenu_mensuel': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            # Correction: frequence_revenu a des choix, donc Select
            'frequence_revenu': forms.Select(attrs={'class': 'form-select'}), 
            'nom_employeur': forms.TextInput(attrs={'class': 'form-input'}),
            'anciennete_emploi': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
        }

    # Nettoyage des champs pour ajouter des contraintes de validation
    def clean_date_naissance(self):
        date_naissance = self.cleaned_data.get('date_naissance')
        if date_naissance and date_naissance > timezone.now().date():
            raise forms.ValidationError("La date de naissance ne peut pas être dans le futur.")
        return date_naissance

    def clean_revenu_mensuel(self):
        revenu_mensuel = self.cleaned_data.get('revenu_mensuel')
        if revenu_mensuel is not None and revenu_mensuel < 0:
            raise forms.ValidationError("Le revenu mensuel ne peut pas être négatif.")
        return revenu_mensuel
    

# Formset pour les documents du client
ClientDocumentFormSet = inlineformset_factory(
    Client, 
    ClientDocument, 
    fields=('type_document', 'fichier'), 
    extra=1, # Commence avec 1 champ vide
    can_delete=True,
    widgets={
        'type_document': forms.Select(attrs={'class': 'form-select'}),
        'fichier': forms.FileInput(attrs={'class': 'form-input'}), 
         # Ajout du widget pour 'description'
    }
)


# Formulaire Compte Client
class CompteForm(forms.ModelForm):
    """
    Formulaire pour ouvrir ou modifier un compte.
    """
    class Meta:
        model = Compte
        fields = ['client', 'type_compte', 'solde', 'is_active']
        labels = {
            'client': 'Client',
            'type_compte': 'Type de compte',
            'solde': 'Solde initial (modifiable si nouveau compte)',
            'is_active': 'Actif',
        }
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'type_compte': forms.Select(attrs={'class': 'form-select'}),
            'solde': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['solde'].widget.attrs['readonly'] = True
            self.fields['solde'].help_text = "Le solde ne peut être modifié que via les transactions."
        
        if 'initial' in kwargs and 'client' in kwargs['initial']:
             self.fields['client'].widget.attrs['disabled'] = True
             self.fields['client'].queryset = Client.objects.filter(pk=kwargs['initial']['client'])


# Formulaire Mouvement (Dépôt/Retrait/Virement)
class MouvementForm(forms.ModelForm):
    """
    Formulaire pour enregistrer un dépôt, un retrait ou un virement.
    """
    class Meta:
        model = Mouvement
        fields = ['compte', 'type_mouvement', 'montant', 'description', 'compte_destinataire']
        labels = {
            'compte': 'Compte Source',
            'type_mouvement': 'Type de Mouvement',
            'montant': 'Montant',
            'description': 'Description',
            'compte_destinataire': 'Compte Destinataire (si Virement)',
        }
        widgets = {
            'compte': forms.Select(attrs={'class': 'form-select'}),
            'type_mouvement': forms.Select(attrs={'class': 'form-select'}),
            'montant': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
            'compte_destinataire': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['compte_destinataire'].required = False
        
        if 'initial' in kwargs and 'compte' in kwargs['initial']:
             self.fields['compte'].widget.attrs['disabled'] = True
             self.fields['compte'].queryset = Compte.objects.filter(pk=kwargs['initial']['compte'])


    def clean(self):
        cleaned_data = super().clean()
        type_mouvement = cleaned_data.get('type_mouvement')
        montant = cleaned_data.get('montant')
        compte = cleaned_data.get('compte')
        compte_destinataire = cleaned_data.get('compte_destinataire')

        if type_mouvement == 'RETRAIT' and compte:
            if montant > compte.solde:
                self.add_error('montant', "Solde insuffisant pour effectuer ce retrait.")
        
        if type_mouvement == 'VIREMENT':
            if not compte_destinataire:
                self.add_error('compte_destinataire', "Un compte destinataire est requis pour un virement.")
            elif compte and compte_destinataire and compte.pk == compte_destinataire.pk:
                self.add_error('compte_destinataire', "Le compte source et le compte destinataire ne peuvent pas être les mêmes.")
            elif compte and montant > compte.solde:
                self.add_error('montant', "Solde insuffisant pour effectuer ce virement.")

        return cleaned_data

# Formulaire Crédit (Prêt)
# microfinance_project/core_finance/forms.py (ou le chemin de votre fichier forms.py)

from django import forms
from django.utils import timezone # Assurez-vous d'avoir bien importé timezone
from .models import Credit, Compte, Client # Assurez-vous que ces imports sont corrects

class CreditForm(forms.ModelForm):
    """
    Formulaire pour enregistrer une demande de crédit.
    """
    class Meta:
        model = Credit
        fields = ['client', 'compte', 'amount_granted', 'interest_rate', 'duree_mois', 'due_date']
        labels = {
            'client': 'Client',
            'compte': 'Compte de Prélèvement',
            'amount_granted': 'Montant Accordé',
            'interest_rate': 'Taux d\'Intérêt Annuel (%)',
            'duree_mois': 'Durée (Mois)',
            'due_date': 'Date d\'Échéance',
        }
        widgets = {
            # C'est la MODIFICATION CLÉ :
            # Ces champs sont maintenant explicitement définis comme des inputs cachés.
            # Leur valeur sera remplie par votre JavaScript côté client.
            'client': forms.HiddenInput(),
            'compte': forms.HiddenInput(),
            
            # Les autres champs conservent leurs widgets et attributs
            'amount_granted': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': 0}),
            'duree_mois': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'due_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Application des classes CSS génériques aux champs visibles (non cachés)
        for field_name in ['amount_granted', 'interest_rate', 'duree_mois', 'due_date']:
            # Assurez-vous que le champ existe et qu'il n'est pas déjà un HiddenInput si vous modifiez la liste
            if field_name in self.fields:
                current_attrs = self.fields[field_name].widget.attrs
                if 'class' in current_attrs:
                    # Ajoute 'form-input' si ce n'est pas déjà présent
                    if 'form-input' not in current_attrs['class']:
                        current_attrs['class'] += ' form-input'
                else:
                    current_attrs['class'] = 'form-input'

    def clean_due_date(self):
        """
        Valide que la date d'échéance n'est pas dans le passé.
        """
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now().date():
            raise forms.ValidationError("La date d'échéance ne peut pas être dans le passé.")
        return due_date



class RemboursementForm(forms.ModelForm):
    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Cash'),
        ('VIREMENT', 'Virement Bancaire'),
        ('MOBILE_MONEY', 'Mobile Money'),
        # Ajoutez d'autres méthodes si nécessaire
    ]

    # Surcharge du champ methode_paiement
    methode_paiement = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        label='Méthode de Paiement',
        widget=forms.Select(attrs={'class': 'form-select'}) # Utiliser un <select> HTML
    )

    class Meta:
        model = Remboursement
        fields = ['credit', 'montant', 'methode_paiement', 'reference', 'notes']
        labels = {
            'credit': 'Crédit concerné',
            'montant': 'Montant Total du Remboursement',
            'reference': 'Référence Externe',
            'notes': 'Notes',
        }
        widgets = {
            'credit': forms.HiddenInput(),
            'montant': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': 0.01}),
            # 'methode_paiement' est géré ci-dessus, donc pas besoin ici
            'reference': forms.TextInput(attrs={'class': 'form-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        credit = cleaned_data.get('credit')
        montant = cleaned_data.get('montant')
        methode_paiement = cleaned_data.get('methode_paiement')
        reference = cleaned_data.get('reference')

        # Assurez-vous que le crédit et le montant sont présents pour la validation suivante
        if credit and montant is not None:
            # Rafraîchir l'objet crédit depuis la base de données
            # C'est crucial au cas où la valeur a changé depuis le chargement du formulaire
            try:
                credit.refresh_from_db()
            except Credit.DoesNotExist:
                # Gérer le cas où le crédit sélectionné n'existe pas (improbable si l'ID est valide)
                self.add_error('credit', "Le crédit sélectionné n'existe plus.")
                return cleaned_data # Retourner les données nettoyées incomplètes

            if montant <= 0:
                self.add_error('montant', "Le montant du remboursement doit être supérieur à zéro.")

            if montant > credit.remaining_total_due:
                self.add_error('montant', f"Le montant du remboursement ({montant:.2f} XOF) ne peut pas dépasser le solde restant ({credit.remaining_total_due:.2f} XOF).")

            # Validation conditionnelle pour 'reference' basée sur 'methode_paiement'
            if methode_paiement in ['VIREMENT', 'MOBILE_MONEY'] and not reference:
                self.add_error('reference', "La référence est requise pour cette méthode de paiement.")
        elif not credit:
            # Erreur si aucun crédit n'a été sélectionné (même si le champ est caché)
            self.add_error('credit', "Veuillez sélectionner un crédit.")
        elif montant is None:
            # Erreur si le montant est manquant
            self.add_error('montant', "Le montant du remboursement est requis.")

        return cleaned_data
# microfinance_project/core_finance/models.py (Assurez-vous que l'app réelle est bien 'gmycom')
from django.db import models, transaction
from django.contrib.auth.models import User # Pour l'agent
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from decimal import Decimal
import uuid # Pour générer des numéros uniques

# Fonctions utilitaires pour les chemins d'upload
def client_cni_recto_path(instance, filename):
    return f'client_docs/{instance.pk}/cni_recto/{filename}'

def client_cni_verso_path(instance, filename):
    return f'client_docs/{instance.pk}/cni_verso/{filename}'

def client_domicile_path(instance, filename):
    return f'client_docs/{instance.pk}/domicile/{filename}'

def client_document_path(instance, filename):
    return f'client_docs/{instance.client.pk}/others/{filename}'


# Modèle Client
class Client(models.Model):
    SITUATION_MATRIMONIALE_CHOICES = [
        ('C', 'Célibataire'),
        ('M', 'Marié(e)'),
        ('D', 'Divorcé(e)'),
        ('V', 'Veuf(ve)'),
    ]

    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('A', 'Autre'),
    ]
    
    FREQUENCE_REVENU_CHOICES = [
        ('MENSUEL', 'Mensuelle'),
        ('BIMENSUEL', 'Bimestrielle'),
        ('TRIMESTRIEL', 'Trimestrielle'),
        ('SEMESTRIEL', 'Semestrielle'),
        ('ANNUEL', 'Annuelle'),
        ('AUTRE', 'Autre'),
    ]

    # Informations Personnelles (Étape 1 et 2 du formulaire)
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    date_naissance = models.DateField(verbose_name="Date de naissance", null=True, blank=True)
    lieu_naissance = models.CharField(max_length=100, verbose_name="Lieu de naissance", null=True, blank=True)
    nationalite = models.CharField(max_length=100, verbose_name="Nationalité", default="Ivoirienne")
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, verbose_name="Sexe", null=True, blank=True)
    situation_matrimoniale = models.CharField(max_length=1, choices=SITUATION_MATRIMONIALE_CHOICES, verbose_name="Situation Matrimoniale", null=True, blank=True)
    nombre_personnes_charge = models.PositiveIntegerField(default=0, verbose_name="Nombre de personnes à charge", null=True, blank=True)

    # Coordonnées (Étape 2 du formulaire)
    telephone = models.CharField(max_length=20, unique=True, verbose_name="Téléphone Principal")
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name="Email")
    adresse = models.TextField(verbose_name="Adresse Résidentielle")
    adresse_pays = models.CharField(max_length=100, verbose_name="Pays", default="Côte d'Ivoire", null=True, blank=True)

    # Informations Professionnelles et Financières (Étape 3 du formulaire)
    profession = models.CharField(max_length=100, verbose_name="Profession", null=True, blank=True)
    secteur_activite = models.CharField(max_length=100, verbose_name="Secteur d'activité", null=True, blank=True)
    revenu_mensuel = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Revenu Mensuel")
    frequence_revenu = models.CharField(max_length=50, verbose_name="Fréquence des revenus", null=True, blank=True, choices=FREQUENCE_REVENU_CHOICES)
    nom_employeur = models.CharField(max_length=255, verbose_name="Nom de l'employeur / Entreprise", null=True, blank=True)
    anciennete_emploi = models.PositiveIntegerField(verbose_name="Ancienneté (en mois)", null=True, blank=True)

    # Champs administratifs
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de Création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de Dernière Modification")
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Agent Responsable")
    is_active = models.BooleanField(default=True, verbose_name="Client Actif")

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['nom', 'prenom']

    @property
    def get_full_name(self):
        """Retourne le nom complet du client."""
        # Correction: utiliser self.nom et self.prenom au lieu de first_name/last_name
        return f"{self.nom} {self.prenom}".strip() 

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.telephone})"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            # Crée un compte épargne par défaut pour chaque nouveau client
            if not Compte.objects.filter(client=self, type_compte='epargne').exists():
                Compte.objects.create(
                    client=self,
                    type_compte='epargne',
                    solde=Decimal('0.00'),
                    opened_by=self.agent,
                    is_active=True
                )
                print(f"Compte épargne créé automatiquement pour le client {self.nom} {self.prenom}")


# Modèle pour les documents justificatifs
class ClientDocument(models.Model):
    DOCUMENT_TYPES = [
        ('CIN_RECTO', 'Carte d\'Identité Nationale (Recto)'),
        ('CIN_VERSO', 'Carte d\'Identité Nationale (Verso)'),
        ('PASSPORT', 'Passeport'),
        ('PERMIS', 'Permis de Conduire'),
        ('JUST_DOM', 'Justificatif de Domicile'),
        ('BUL_SAL', 'Bulletin de Salaire'),
        ('K_BIS', 'K-bis'),
        ('PHOTO_ID', 'Photo d\'Identité'),
        ('AUTRE', 'Autre'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='documents', verbose_name="Client")
    type_document = models.CharField(max_length=20, choices=DOCUMENT_TYPES, verbose_name="Type de Document")
    fichier = models.FileField(upload_to=client_document_path, verbose_name="Fichier")
    date_telechargement = models.DateTimeField(auto_now_add=True, verbose_name="Date de Téléchargement")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    class Meta:
        verbose_name = "Document Client"
        verbose_name_plural = "Documents Clients"
        unique_together = ('client', 'type_document')

    def __str__(self):
        return f"{self.get_type_document_display()} pour {self.client}"


class Compte(models.Model):
    TYPE_COMPTE_CHOICES = [
        ('epargne', 'Compte Épargne'),
        ('courant', 'Compte Courant'),
    ]
    numero_compte = models.CharField(max_length=20, unique=True, blank=True, verbose_name="Numéro de Compte")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='comptes', verbose_name="Client")
    type_compte = models.CharField(max_length=10, choices=TYPE_COMPTE_CHOICES, verbose_name="Type de Compte")
    solde = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), verbose_name="Solde")
    date_ouverture = models.DateTimeField(auto_now_add=True, verbose_name="Date d'Ouverture")
    opened_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ouvert par")
    is_active = models.BooleanField(default=True, verbose_name="Compte Actif")

    class Meta:
        verbose_name = "Compte"
        verbose_name_plural = "Comptes"
        ordering = ['-date_ouverture']

    def __str__(self):
        return f"{self.numero_compte} - {self.client.nom} {self.client.prenom} ({self.get_type_compte_display()})"

    def save(self, *args, **kwargs):
        if not self.numero_compte:
            self.numero_compte = f"COMPTE-{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)

    def deposer(self, montant, agent=None, description="Dépôt"):
        if montant <= 0:
            raise ValueError("Le montant du dépôt doit être positif.")
        with transaction.atomic():
            solde_avant = self.solde
            self.solde += montant
            self.save(update_fields=['solde'])
            HistoriqueTransaction.objects.create(
                compte=self,
                type_operation='DEPOT',
                montant=montant,
                solde_avant=solde_avant,
                solde_apres=self.solde,
                description=description,
                agent=agent
            )

    def retirer(self, montant, agent=None, description="Retrait"):
        if montant <= 0:
            raise ValueError("Le montant du retrait doit être positif.")
        if self.solde < montant:
            raise ValueError("Solde insuffisant pour ce retrait.")
        with transaction.atomic():
            solde_avant = self.solde
            self.solde -= montant
            self.save(update_fields=['solde'])
            HistoriqueTransaction.objects.create(
                compte=self,
                type_operation='RETRAIT',
                montant=montant,
                solde_avant=solde_avant,
                solde_apres=self.solde,
                description=description,
                agent=agent
            )
    def transferer(self, montant, compte_destinataire, agent=None, description="Virement"):
        if montant <= 0:
            raise ValueError("Le montant du virement doit être positif.")
        if self.solde < montant:
            raise ValueError("Solde insuffisant pour ce virement.")
        if self.pk == compte_destinataire.pk:
            raise ValueError("Le compte source et le compte destinataire ne peuvent pas être les mêmes.")

        with transaction.atomic():
            self.solde -= montant
            compte_destinataire.solde += montant
            self.save(update_fields=['solde'])
            compte_destinataire.save(update_fields=['solde'])

            # Création du Mouvement d'abord si Mouvement est la source de vérité pour les virements
            mouvement_instance = Mouvement.objects.create( #
                compte=self, #
                type_mouvement='VIREMENT', #
                montant=montant, #
                description=description, #
                compte_destinataire=compte_destinataire, #
                agent=agent #
            )

            HistoriqueTransaction.objects.create(
                compte=self,
                type_operation='VIREMENT',
                montant=montant,
                solde_avant=self.solde + montant,
                solde_apres=self.solde,
                description=f"{description} vers {compte_destinataire.numero_compte}",
                agent=agent,
                mouvement=mouvement_instance # Lien vers le mouvement créé
            )
            HistoriqueTransaction.objects.create(
                compte=compte_destinataire,
                type_operation='VIREMENT_RECU',
                montant=montant,
                solde_avant=compte_destinataire.solde - montant,
                solde_apres=compte_destinataire.solde,
                description=f"{description} de {self.numero_compte}",
                agent=agent,
                mouvement=mouvement_instance # Lien vers le même mouvement créé
            )


class Mouvement(models.Model):
    TYPE_MOUVEMENT_CHOICES = [
        ('DEPOT', 'Dépôt'),
        ('RETRAIT', 'Retrait'),
        ('VIREMENT', 'Virement'),
    ]
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='mouvements', verbose_name="Compte Source")
    type_mouvement = models.CharField(max_length=10, choices=TYPE_MOUVEMENT_CHOICES, verbose_name="Type de Mouvement")
    montant = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Montant")
    date_mouvement = models.DateTimeField(auto_now_add=True, verbose_name="Date du Mouvement")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    compte_destinataire = models.ForeignKey(Compte, on_delete=models.SET_NULL, null=True, blank=True, related_name='mouvements_recus', verbose_name="Compte Destinataire")
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Agent Enregistreur")

    class Meta:
        verbose_name = "Mouvement"
        verbose_name_plural = "Mouvements"
        ordering = ['-date_mouvement']

    def __str__(self):
        return f"{self.get_type_mouvement_display()} de {self.montant} sur {self.compte.numero_compte}"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        if is_new:
            with transaction.atomic():
                if self.type_mouvement == 'DEPOT':
                    self.compte.deposer(self.montant, agent=self.agent, description=self.description)
                elif self.type_mouvement == 'RETRAIT':
                    self.compte.retirer(self.montant, agent=self.agent, description=self.description)
                elif self.type_mouvement == 'VIREMENT':
                    if not self.compte_destinataire:
                        raise ValueError("Le compte destinataire est requis pour un virement.")
                    self.compte.transferer(self.montant, self.compte_destinataire, agent=self.agent, description=self.description)
                    super().save(*args, **kwargs) # Sauvegarde le mouvement.
        else:
            super().save(*args, **kwargs)


class Credit(models.Model):
    CREDIT_STATUSES = [
        ('PENDING', 'En Attente'),
        ('ACTIVE', 'Actif'),
        ('REPAID', 'Remboursé'),
        ('OVERDUE', 'En Retard'),
        ('REJECTED', 'Rejeté'),
    ]
    numero_credit = models.CharField(max_length=20, unique=True, blank=True, verbose_name="Numéro de Crédit")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='credits', verbose_name="Client")
    compte = models.ForeignKey(Compte, on_delete=models.SET_NULL, null=True, blank=True, related_name='credits_associes', verbose_name="Compte Client")
    amount_granted = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Montant Accordé")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Taux d'Intérêt (%)") # Taux annuel
    duree_mois = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="Durée (Mois)")
    date_demande = models.DateTimeField(auto_now_add=True, verbose_name="Date de Demande")
    due_date = models.DateField(verbose_name="Date d'Échéance Finale")
    status = models.CharField(max_length=10, choices=CREDIT_STATUSES, default='PENDING', verbose_name="Statut du Crédit")
    total_interest_expected = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), verbose_name="Intérêts Totaux Attendus")
    total_expected_repayment = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), verbose_name="Montant Total Attendu")
    amount_repaid = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), verbose_name="Montant Total Remboursé")
    granted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Accordé par")

    class Meta:
        verbose_name = "Crédit"
        verbose_name_plural = "Crédits"
        ordering = ['due_date']

    def __str__(self):
        return f"Crédit {self.numero_credit} pour {self.client.nom} {self.client.prenom}"

    @property
    def monthly_payment(self):
        if self.duree_mois > 0 and self.amount_granted > 0:
            monthly_interest_rate = self.interest_rate / Decimal('1200')
            if monthly_interest_rate > 0:
                pmt = (self.amount_granted * monthly_interest_rate * (1 + monthly_interest_rate)**self.duree_mois) / \
                      (((1 + monthly_interest_rate)**self.duree_mois) - 1)
                return pmt.quantize(Decimal('0.01'))
            else:
                return (self.amount_granted / self.duree_mois).quantize(Decimal('0.01'))
        return Decimal('0.00')

    @property
    def remaining_total_due(self):
        return (self.total_expected_repayment - self.amount_repaid).quantize(Decimal('0.01'))

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        
        if is_new and not self.numero_credit:
            self.numero_credit = f"CREDIT-{str(uuid.uuid4())[:8].upper()}"
        
        # Calcul des intérêts et total attendu
        if is_new or 'update_fields' not in kwargs or any(field in kwargs['update_fields'] for field in ['amount_granted', 'interest_rate', 'duree_mois']):
            if self.duree_mois > 0 and self.amount_granted > 0:
                total_expected_repayment_calculated = (self.monthly_payment * self.duree_mois).quantize(Decimal('0.01'))
                self.total_expected_repayment = total_expected_repayment_calculated
                self.total_interest_expected = (self.total_expected_repayment - self.amount_granted).quantize(Decimal('0.01'))
            else:
                self.total_interest_expected = Decimal('0.00')
                self.total_expected_repayment = self.amount_granted.quantize(Decimal('0.01'))

        # Mise à jour du statut selon remboursement et date échéance
        if self.amount_repaid >= self.total_expected_repayment and self.status != 'REPAID':
            self.status = 'REPAID'
        elif self.amount_repaid < self.total_expected_repayment and self.status == 'REPAID':
            self.status = 'ACTIVE'

        if self.status == 'ACTIVE' and self.due_date and self.due_date < timezone.now().date():
            self.status = 'OVERDUE'

        super().save(*args, **kwargs)

        # Décaissement (prêt) : ajout d'argent sur le compte client lié
        if is_new and self.status != 'REJECTED' and self.compte:
            with transaction.atomic():
                solde_avant = self.compte.solde
                try:
                    self.compte.deposer(self.amount_granted, agent=self.granted_by, description=f"Décaissement crédit {self.numero_credit}")
                    HistoriqueTransaction.objects.create(
                        credit=self,
                        compte=self.compte,
                        type_operation='DECAISSEMENT_CREDIT',
                        montant=self.amount_granted,
                        solde_avant=solde_avant,
                        solde_apres=self.compte.solde,
                        description=f"Décaissement du crédit {self.numero_credit} vers client {self.client.nom} {self.client.prenom}",
                        agent=self.granted_by
                    )
                    self.status = 'ACTIVE'
                    super().save(update_fields=['status'])
                except ValueError as e:
                    self.status = 'REJECTED'
                    super().save(update_fields=['status'])
                    print(f"Erreur de décaissement (dépôt) crédit {self.numero_credit}: {e}")
    
# Corrected sender reference for post_delete signal
@receiver(post_delete, sender='gmycom.Remboursement')
def update_credit_on_remboursement_delete(sender, instance, **kwargs):
    # Réduit le montant remboursé sur le crédit associé
    credit = instance.credit
    credit.amount_repaid -= instance.montant
    credit.save() # La méthode save() du Credit mettra à jour son statut si nécessaire

    HistoriqueTransaction.objects.filter(remboursement=instance, type_operation='REMBOURSEMENT').delete()


# Corrected sender reference for post_delete signal
@receiver(post_delete, sender='gmycom.Credit')
def update_transaction_history_on_credit_delete(sender, instance, **kwargs):
    # Supprime toutes les entrées d'historique de transaction liées à ce crédit
    HistoriqueTransaction.objects.filter(credit=instance).delete()


class Remboursement(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Cash'),
        ('VIREMENT', 'Virement Bancaire'),
        ('MOBILE_MONEY', 'Mobile Money'),
    ]
    
    numero_remboursement = models.CharField(max_length=20, unique=True, blank=True, verbose_name="Numéro de Remboursement")
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, related_name='remboursements', verbose_name="Crédit")
    montant = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Montant Remboursé")
    date_remboursement = models.DateTimeField(auto_now_add=True, verbose_name="Date du Remboursement")
    methode_paiement = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default="CASH", verbose_name="Méthode de Paiement")
    reference = models.CharField(max_length=100, blank=True, null=True, verbose_name="Référence Externe")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Agent Enregistreur")

    class Meta:
        verbose_name = "Remboursement"
        verbose_name_plural  = "Remboursements"
        ordering = ['-date_remboursement']

    def __str__(self):
        return f"Remb. {self.montant} pour Crédit {self.credit.numero_credit}"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        if is_new and not self.numero_remboursement:
            self.numero_remboursement = f"RMB-{str(uuid.uuid4())[:8].upper()}"

        with transaction.atomic():
            # Mise à jour du solde du compte client (retrait de la somme remboursée)
            if is_new and self.credit.compte:
                compte = self.credit.compte
                if compte.solde < self.montant:
                    raise ValueError("Solde insuffisant sur le compte pour le remboursement.")
                solde_avant = compte.solde
                compte.retirer(self.montant, agent=self.agent, description=f"Remboursement crédit {self.credit.numero_credit}")

            super().save(*args, **kwargs) # Sauvegarde du remboursement

            if is_new:
                # Mise à jour du montant remboursé sur le crédit
                self.credit.amount_repaid += self.montant
                self.credit.save()

                HistoriqueTransaction.objects.create(
                    remboursement=self,
                    credit=self.credit,
                    compte=self.credit.compte,
                    type_operation='REMBOURSEMENT',
                    montant=self.montant,
                    solde_avant=solde_avant if self.credit.compte else None,
                    solde_apres=self.credit.compte.solde if self.credit.compte else None,
                    description=f"Remboursement de {self.montant} XOF pour crédit {self.credit.numero_credit} par {self.credit.client.get_full_name}",
                    agent=self.agent
                )


class HistoriqueTransaction(models.Model):
    TYPE_OPERATION_CHOICES = [
        ('DEPOT', 'Dépôt sur Compte Client'), # Ajout de précision
        ('RETRAIT', 'Retrait sur Compte Client'), # Ajout de précision
        ('VIREMENT', 'Virement Sortant Client'), # Ajout de précision
        ('VIREMENT_RECU', 'Virement Entrant Client'), # Ajout de précision
        ('DECAISSEMENT_CREDIT', 'Décaissement Crédit'), # Renommé pour plus de clarté
        ('REMBOURSEMENT', 'Remboursement Crédit'),
    ]
    compte = models.ForeignKey(Compte, on_delete=models.SET_NULL, null=True, blank=True, related_name='historique_compte', verbose_name="Compte Client concerné") # Renommé pour clarté
    credit = models.ForeignKey(Credit, on_delete=models.SET_NULL, null=True, blank=True, related_name='historique_credit', verbose_name="Crédit concerné")
    remboursement = models.ForeignKey(Remboursement, on_delete=models.SET_NULL, null=True, blank=True, related_name='historique_remboursement', verbose_name="Remboursement concerné")
    mouvement = models.ForeignKey(Mouvement, on_delete=models.SET_NULL, null=True, blank=True, related_name='historique_mouvement', verbose_name="Mouvement de Compte Client concerné") # Renommé pour clarté

    type_operation = models.CharField(max_length=20, choices=TYPE_OPERATION_CHOICES, verbose_name="Type d'Opération")
    montant = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Montant")
    date_operation = models.DateTimeField(auto_now_add=True, verbose_name="Date d'Opération")
    solde_avant = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Solde Avant Opération (Compte Client)") # Renommé
    solde_apres = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Solde Après Opération (Compte Client)") # Renommé
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Agent")

    class Meta:
        verbose_name = "Historique de Transaction"
        verbose_name_plural = "Historiques de Transactions"
        ordering = ['-date_operation']

    def __str__(self):
        return f"{self.get_type_operation_display()} - {self.montant} XOF le {self.date_operation.strftime('%Y-%m-%d %H:%M')}"

    def clean(self):    
        pass # La logique de validation sera plus complexe ou retirée si non pertinente.
      
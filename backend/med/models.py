from django.db import models
from users.models import CustomUser

class PersonneAContacter(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)  

    def __str__(self):
        return f"{self.nom} {self.prenom}"

 
class Etablissement(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField()
    telephone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nom} - {self.adresse}"


class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient_profile')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_de_naissance = models.DateField()
    adresse = models.TextField()
    telephone = models.CharField(max_length=15)  
    nss = models.CharField(max_length=15, unique=True)  # Ajout de `unique` pour éviter les doublons
    mutuelle = models.CharField(max_length=100, blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    personne_a_contacter = models.ForeignKey(
        'PersonneAContacter', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="patients"
    )  
    def __str__(self):
        return f"{self.nom} {self.prenom} (NSS : {self.nss})"


class DPI(models.Model): 
    ETATS= [('ouvert', 'ouvert'), ('fermé', 'fermé')]
    etat = models.CharField(default='ouvert', max_length=10, choices = ETATS)
    patient = models.OneToOneField(
        'Patient', 
        on_delete=models.CASCADE, 
        related_name='dossier_patient',  
        help_text="Le patient associé à ce DSI"
    )

    def __str__(self):
        return f"Dossier patient de {self.patient.nom} {self.patient.prenom}"


class Traitement(models.Model):
    nom = models.CharField(max_length=100)
    dose = models.CharField(max_length=100)  # Exemple : "500mg"
    consommation = models.CharField(
        max_length=100, 
        help_text="Par exemple : '3 comprimés'"
    )
    def __str__(self):
        return f"{self.nom} ({self.dose})"


class Ordonnance(models.Model):
    validee = models.BooleanField(default=False)
    dpi = models.ForeignKey(
        'DPI', 
        on_delete=models.CASCADE,
        related_name='dpi', 
        help_text="DPI associé à cette ordonnance"
    )
    date_emission = models.DateField("Date d'émission", auto_now_add=True)
    traitements = models.ManyToManyField(
        'Traitement', 
        related_name='ordonnances', 
        help_text="Liste des traitements inclus dans cette ordonnance"
    )

    def __str__(self):
        return f"Ordonnance du {self.date_emission} - {self.patient.nom} {self.patient.prenom}"


class Examen(models.Model):
    prescription = models.CharField(
        max_length=255,
        help_text="Description de la prescription pour cet examen"
    )
    date_emission = models.DateField(
        "Date d'émission",
        auto_now_add=False
    )
    consultation = models.ForeignKey(
        'Consultation',
        on_delete=models.CASCADE,
        related_name='examens_from_examen',
        help_text="Consultation à laquelle cet examen est associé"
    )

    def __str__(self):
        return f"Examen : {self.prescription} pour la consultation du {self.consultation.date}"


class Consultation(models.Model):
    date = models.DateField(
        "Date de consultation",
        auto_now_add=True,
        help_text="Date à laquelle la consultation a eu lieu"
    )
    resume = models.CharField(
        max_length=2500,
        help_text="Résumé de la consultation"
    )
    ordonnance = models.ForeignKey(
        'Ordonnance',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='consultations',
        help_text="Ordonnance liée à cette consultation (optionnelle)"
    )
    examens = models.ManyToManyField(
        'Examen',  
        blank=True,
        related_name='consultations_from_examens',
        help_text="Examens associés à cette consultation"
    )
    dpi = models.ForeignKey(
        'DPI',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        default=None,
        related_name='consultations',
        help_text="DPI associé à cette consultation"
    )

    def __str__(self):
        return f"Consultation du {self.date}"


class BilanBiologique(Examen):
    resultat = models.TextField(
        help_text="Résultat du bilan biologique"
    )


class BilanRadiologique(Examen):
    compte_rendu = models.TextField(
        help_text="Compte-rendu du bilan radiologique"
    )
    image_url = models.ImageField(upload_to='radio/', blank=True, null=True)

class Medecin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    specialite = models.CharField(max_length=100)
    etablissement = models.ForeignKey(
        'Etablissement',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='medecins'
    )

class Soin(models.Model):
    etat = models.CharField(max_length=100, help_text="État associé")
    medicament = models.CharField(max_length=255, help_text="Nom du médicament")
    autre = models.TextField(help_text="Autre information supplémentaire", null=True, blank=True)
    date = models.DateField(auto_now_add=False, help_text="Date de création du soin")
    dpi = models.ForeignKey(
        DPI,
        on_delete=models.CASCADE,
        related_name='soins',
        help_text="DPI auquel ce soin est associé"
    )
    def __str__(self):
        return f"Soin : {self.medicament} ({self.etat}) - {self.date}"
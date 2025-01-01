from django.db import models
from django.contrib.auth.models import AbstractUser



class PersonneAContacter(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)  

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('medecin', 'Médecin'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='Patient')

    def __str__(self):
        return self.username


 
class Etablissement(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField()
    telephone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nom} - {self.adresse}"

# class Utilisateur(models.Model):
#     username = models.CharField(max_length=20)
#     password = models.CharField(max_length=30)
#     telephone = models.CharField(max_length=15)
#     etablissement = models.ForeignKey(
#         Etablissement,  # Relation un-à-plusieurs
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="utilisateurs"
#     )




class Patient(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_de_naissance = models.CharField(max_length=100)
    adresse = models.TextField()
    telephone = models.CharField(max_length=15)  
    nss = models.CharField(max_length=15, unique=True)  # Ajout de `unique` pour éviter les doublons
    mutuelle = models.CharField(max_length=100, blank=True, null=True)  # Optionnel
    personne_a_contacter = models.ForeignKey(
        'PersonneAContacter', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="patients"
    )  


    def __str__(self):
        return f"{self.nom} {self.prenom} (NSS : {self.nss})"

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
    STATUT_CHOICES = [
        ('distribuee', 'Distribuée'),
        ('en_attente', 'En attente'),
        ('validee', 'Validée'),
    ]
    consultation = models.ForeignKey(
        'Consultation', 
        on_delete=models.CASCADE,  
        related_name='ordonnances',  
        help_text="Consultation associée à cette ordonnance"
    )
    
    date_emission = models.DateField("Date d'émission", auto_now_add=True)
    status = models.CharField(
        max_length=100, 
        choices=STATUT_CHOICES, 
        default='en_attente', 
        help_text="Statut actuel de l'ordonnance"
    )
    traitements = models.ManyToManyField(
        'Traitement', 
        related_name='ordonnances', 
        help_text="Liste des traitements inclus dans cette ordonnance"
    )

    def __str__(self):
        return f"Ordonnance du {self.date_emission} pour consultation {self.consultation.id}"







class DPI(models.Model):
    patient = models.OneToOneField(
        'Patient', 
        on_delete=models.CASCADE, 
        related_name='dossier_patient',  # Un nom inversé unique
        help_text="Le patient associé à ce DSI"
    )
    # utilisateur = models.OneToOneField(
    #     'Utilisateur', 
    #     on_delete=models.CASCADE, 
    #     related_name='dossier_utilisateur',  # Un nom inversé unique
    #     help_text="L'utilisateur associé à ce DSI"
    # )

    def __str__(self):
        return f"Dossier patient de {self.patient.nom} {self.patient.prenom}"


class Examen(models.Model):
    idc = models.IntegerField()  # L'id de la consultation
    consigne = models.TextField()  # La consigne de l'examen

    def __str__(self):
        return f"Examen pour la consultation {self.idd}"


class Consultation(models.Model):
    id = models.AutoField(primary_key=True)
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
    dpi = models.ForeignKey(
        'DPI',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        default=None,
        related_name='consultations',
        help_text="DPI associé à cette consultation"
    )
    examens = models.ManyToManyField(
        Examen,
        blank=True,
        related_name='consultations',
        help_text="Examens associés à cette consultation"
    )

    def __str__(self):
        return f"Consultation du {self.date}"




from django.db import models

class BilanBiologique(models.Model):
    idc = models.IntegerField()  # l'id de la consultation
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
        related_name='bilans_biologiques',
        help_text="Consultation à laquelle ce bilan biologique est associé"
    )
    resultat = models.TextField(
        help_text="Résultat du bilan biologique"
    )

    def __str__(self):
        return f"Bilan Biologique : {self.prescription} pour la consultation du {self.consultation.date}"

class BilanRadiologique(models.Model):
    idc = models.IntegerField()  # l'id de la consultation
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
        related_name='bilans_radiologiques',
        help_text="Consultation à laquelle ce bilan radiologique est associé"
    )
    compte_rendu = models.TextField(
        help_text="Compte-rendu du bilan radiologique"
    )
    image_url = models.URLField(
        max_length=200,
        null=True,
        blank=True,
        help_text="Lien vers l'image radiologique (optionnel)"
    )

    def __str__(self):
        return f"Bilan Radiologique : {self.prescription} pour la consultation du {self.consultation.date}"


class Medecin(models.Model):
    id = models.AutoField(primary_key=True)  # Définir un champ id explicite si nécessaire
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr {self.nom} {self.prenom} ({self.specialite})"

class test(models.Model):
    id = models.AutoField(primary_key=True)  # Définir un champ id explicite si nécessaire





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

     
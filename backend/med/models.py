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
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_de_naissance = models.DateField()
    adresse = models.TextField()
    telephone = models.CharField(max_length=15)  
    nss = models.CharField(max_length=15, unique=True)  # Ajout de `unique` pour éviter les doublons
    mutuelle = models.CharField(max_length=100, blank=True, null=True) 
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
    antecedents_medicaux = models.TextField(default= 'Aucun antecedent',help_text="Antecedents medicaux du patient")
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
    frequence = models.IntegerField(
        verbose_name="Fréquence (en jours)", 
        help_text="Par exemple : tous les 3 jours"
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
    dpi = models.ForeignKey(
        DPI,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        default=None,
        related_name='consultations',
        help_text="DPI associé à cette consultation"
    )

    def __str__(self):
        return f"Consultation du {self.date}"



class Bilan(models.Model):
    prescription = models.CharField(
        max_length=255,
        help_text="Description de la prescription pour cet examen"
    )
    date_emission = models.DateField(
        "Date d'émission",
        auto_now_add=True
    )
    consultation = models.ForeignKey(
        'Consultation',
        on_delete=models.CASCADE,
        related_name='bilans',
        help_text="Consultation à laquelle ce bilan est associé"
    )

    def __str__(self):
        return f"Bilan : {self.prescription} pour la consultation du {self.consultation.date}"


class BilanBiologique(Bilan):
    resultat = models.TextField(
        help_text="Résultat du bilan biologique"
    )


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

class test(models.Model):
    id = models.AutoField(primary_key=True)  # Définir un champ id explicite si nécessaire


class BilanRadiologique(Bilan):
    compte_rendu = models.TextField(
        help_text="Compte-rendu du bilan radiologique"
    )
    image_url = models.URLField(
        max_length=200,
        null=True,
        blank=True,
        help_text="Lien vers l'image radiologique (optionnel)"
    )
from django.db import models

class PersonneAContacter(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)  

    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
class Patient(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_de_naissance = models.DateField("Date de naissance")
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
    medecins = models.ManyToManyField(
        'Medecin', 
        blank=True,  # `null=True` n'est pas nécessaire pour ManyToManyField
        related_name="patients"
    )

    def __str__(self):
        return f"{self.nom} {self.prenom} (NSS : {self.nss})" 

class DPI(models.Model):
    antecedants_medicaux = models.TextField(default= 'Aucun antecedant',help_text="Antecedants medicaux du patient")
    patient = models.OneToOneField(
        'Patient', 
        on_delete=models.CASCADE, 
        related_name='dossier_patient',  # Un nom inversé unique
        help_text="Le patient associé à ce DSI"
    )

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
        related_name='ordonnances', 
        help_text="DPI associé à cette ordonnance"
    )
    date_emission = models.DateField("Date d'émission", auto_now_add=True)
    traitements = models.ManyToManyField(
        'Traitement', 
        related_name='ordonnances', 
        help_text="Liste des traitements inclus dans cette ordonnance"
    )

    def __str__(self):
        return f"Ordonnance du {self.date_emission}"


class Distribution(models.Model):
    ordonnance = models.ForeignKey(
        'Ordonnance', 
        on_delete=models.CASCADE, 
        related_name='distributions', 
        help_text="Ordonnance associée à cette distribution"
    )
    traitement = models.ForeignKey(
        'Traitement', 
        on_delete=models.CASCADE, 
        related_name='distributions', 
        help_text="Médicament délivré"
    )
    quantite = models.IntegerField(help_text="Quantité délivrée")
    date_distribution = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantite}x {self.traitement.nom} - {self.date_distribution}"


class Medecin(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr {self.nom} {self.prenom} ({self.specialite})"
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLES = [
        ('Administratif', 'Administratif'),
        ('Médecin', 'Médecin'),
        ('Infirmier', 'Infirmier'),
        ('Laborantin', 'Laborantin'),
        ('Radiologue', 'Radiologue'),
        ('Patient', 'Patient'),
    ]
    role = models.CharField(max_length=20, choices=ROLES)

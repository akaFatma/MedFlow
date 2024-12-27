from django.contrib import admin
from .models import CustomUser  # Assure-toi que CustomUser est bien importé

# Définition de la classe CustomUserAdmin
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')  # Champs à afficher dans l'admin
    list_filter = ('role',)  # Filtrer par rôle dans l'admin

# Enregistrement du modèle CustomUser avec la classe CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
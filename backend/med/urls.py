from django.urls import path
from . import views  # Assurez-vous que 'views' est bien importé

urlpatterns = [
    path('', views.home, name='home'),  # Route pour la page d'accueil
    path('creerdpi/', views.creer_dpi, name='creerdpi'),  # Modifier ici pour utiliser creer_dpi
    path('creerrdpi/', views.creerr_dpi, name='creerrdpi'),
]

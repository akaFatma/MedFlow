# projetigl/urls.py

from django.contrib import admin
from django.urls import path
from med import views  # Importation correcte de 'views' depuis l'application 'med'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Route pour la page d'accueil
    path('creerdpi/', views.creer_dpi, name='creerdpi'),
    path('creerrdpi/', views.creerr_dpi, name='creerrdpi'),
]

# projetigl/urls.py

from django.contrib import admin
from django.urls import path
from med import views  # Assurez-vous que 'views' est bien importé depuis l'application 'med'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Route pour la page d'accueil
    path('creerrdpi/', views.creerr_dpi, name='creerrdpi'),
    path('consultation/', views.commencer_consultation, name='consultation'),  # C'est ici la route pour commencer la consultation
    path('soin/', views.rediger_soin, name='soin'),
]

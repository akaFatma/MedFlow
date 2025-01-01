# med/urls.py

from django.urls import path
from . import views  # Assurez-vous que 'views' est bien importé depuis l'application 'med'

urlpatterns = [
    path('creerrdpi/', views.creerr_dpi, name='creerrdpi'),
    path('consultation/', views.commencer_consultation, name='consultation'),  # Route pour commencer la consultation
    path('soin/', views.rediger_soin, name='soin'), # Route pour commencer le soin
]

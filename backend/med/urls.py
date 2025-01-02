from django.urls import path
from . import views

urlpatterns = [
    path('creerdpi', views.creer_dpi, name='creerdpi'),
    path('patients', views.list_patients, name='list des patients'),
    path('patients/search', views.list_patients_filtered, name='list des patients recherchée'),
    path('patients/nss', views.get_dpi, name='dpi'),
    path('consultation', views.commencer_consultation, name='consultation'),  # Route pour commencer la consultation
    path('soin', views.rediger_soin, name='soin'), # Route pour commencer le soin
]

from django.urls import path
from . import views

urlpatterns = [
    path('creerdpi', views.creer_dpi, name='creerdpi'),
    path('patients', views.list_patients, name='list des patients'),
    path('patients/search', views.list_patients_filtered, name='list des patients recherchée'),
    path('patients/nss', views.get_dpi, name='dpi'),
    path('consultation', views.commencer_consultation, name='consultation'),  # Route pour commencer la consultation
    path('soin', views.rediger_soin, name='soin'), # Route pour commencer le soin
    path('medecin', views.MedecinView, name='medecin'), 
    path('consultationHistory', views.get_patient_consultations, name='liste des consultations'),
    path('consultationContent', views.get_user_info, name='liste des consultations'),
    path('soinHistory', views.get_patient_soins, name='liste des soins'),
    path('getnss', views.get_nss_info, name='getnss'),
    path('bilansbiologiques', views.export_bilans_bio, name='export bilans'),
    path('bilansradiologiques', views.export_bilans_radio, name='export bilans'),
    path('bio-pres', views.envoi_pres_bio, name='prescription'),
    path('radio-pres', views.envoi_pres_radio, name='prescription'),
    path('saisie-bilan-bio', views.remplir_bilan_bio, name='remplir bilan'),
    path('saisie-bilan-radio', views.remplir_bilan_radio, name='remplir bilan'),
    path('image-radio', views.get_radiography_image, name='Envoi image radio'),
    
    path('ordonnance/<int:id>/', views.get_ordonnance, name='get_ordonnance'),
    path('ordonnances/<int:id>/valider', views.valider_ordonnance, name='valider_ordonnance'),
    path('distributions', views.distribuer_medicament, name='distribuer_medicament'),
    
]

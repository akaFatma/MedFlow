from django.urls import path
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path
from django.views.generic import RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
    ),
    public=True,
)

urlpatterns = [
    path('', RedirectView.as_view(url='/swagger/', permanent=False)),
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
    path('saisie-bilan-bio', views.remplir_bilan_bio, name='remplir bilan bio'),
    path('saisie-bilan-radio', views.remplir_bilan_radio, name='remplir bilan radio'),
    path('image-radio', views.get_radiography_image, name='Envoi image radio'),
    path('ordonnance/<int:id>/', views.get_ordonnance, name='get_ordonnance'),
    path('ordonnances/<int:id>/valider', views.valider_ordonnance, name='valider_ordonnance'),
    path('distributions', views.distribuer_medicament, name='distribuer_medicament'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    
]

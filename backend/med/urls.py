from django.urls import path
from . import views

urlpatterns = [
    path('creerdpi', views.creer_dpi, name='creerdpi'),
    path('patients', views.list_patients, name='list des patients'),
    path('patients/search', views.list_patients_filtered, name='list des patients recherchée'),
    path('patients/nss', views.get_dpi, name='dpi'),
]

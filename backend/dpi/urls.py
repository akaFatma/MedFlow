from django.urls import path
from . import views


urlpatterns = [
    path('patients', views.list_patients, name='list_patients'),
    path('create', views.create_patient_with_dpi, name='creer'),
    path('patients/<str:nss>', views.get_dpi, name='dpi'),
    path('test', views.get_dpi_by_qr, name='qr'),
]

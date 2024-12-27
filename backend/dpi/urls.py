from django.urls import path
from . import views


urlpatterns = [
    path('patients', views.list_patients, name='list des patients'),
    path('patients/search', views.list_patients_filtered, name='list des patients recherchée'),
    path('patients/nss/<str:nss>', views.get_dpi, name='dpi'),
    path('patients/qrcode', views.get_dpi_by_qr, name='qr'),
    path('test', views.qr_code, name='qr'), #pour generer le code qr, probablement sera fusionné avec creer dpi
    path('create', views.create_patient_with_dpi, name='creer'),#utilisée juste pour tester
]

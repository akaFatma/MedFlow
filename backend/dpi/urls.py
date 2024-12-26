from django.urls import path
from . import views


urlpatterns = [
    path('patients', views.list_patients, name='list_patients'),
    path('patients/nss/<str:nss>', views.get_dpi, name='dpi'),
    path('patients/qrcode', views.get_dpi_by_qr, name='qr'),
    path('test', views.qr_code, name='qr'), #pour generer le code qr, probablement sera fusionné avec creer dpi
    path('create', views.create_patient_with_dpi, name='creer'),#utilisée juste pour tester
        path('ordonnances/<int:id>/valider/', views.valider_ordonnance, name='valider_ordonnance'),
    path('distributions/', views.distribuer_medicament, name='distribuer_medicament'),
]

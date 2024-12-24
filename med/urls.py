from django.urls import path
from . import views  # Assurez-vous que 'views' est bien importé

urlpatterns = [
    path('creerdpi/', views.creer_dpi, name='creerdpi'),  # Modifier ici pour utiliser creer_dpi
]

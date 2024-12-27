"""
URL configuration for tp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.contrib import admin
from igl import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    #path('demander_certificat/<str:patient_nss>/', views.demander_certificat_medical, name='demander_certificat'),
   # path('ajouter_patient/', views.ajouter_patient, name='ajouter_patient'),
   # path('consulter_dpi/<int:dpi_id>/', views.consulter_dpi, name='consulter_dpi'),
    path('remplir_bilan/<int:consultation_id>/<str:type_bilan>/', views.remplir_bilan, name='remplir_bilan'),
    path('generer_graphique_bilan_biologique/<int:consultation_id>/', views.generer_graphique_bilan_biologique, name='generer_graphique_bilan_biologique'), 
    path('ajouter_consultation/', views.ajouter_consultation, name='ajouter_consultation'),
    path('admin/', admin.site.urls),  # Utilise admin.site.urls pour l'admin
    # autres chemins d'URL à ajouter ici
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

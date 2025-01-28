from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from users.models import CustomUser
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import BilanBiologique, Consultation, Patient, PersonneAContacter, DPI 
import json

class DpiTestCase(TestCase):
    def setUp(self):
        # Création d'une personne à contacter pour les tests
        self.personne_a_contacter = PersonneAContacter.objects.create(
            nom="Touat", prenom="Malak", telephone="0123456789"
        )
        
        # Création de données fictives pour le test
        self.patient_data = {
            "nom": "Kimouche",
            "prenom": "Yasmine",
            "date_naissance": "2003-10-10",
            "telephone": "0123456789",
            "nss": "12168745918745",
            "mutuelle": "Mutuelle Test",
            "adr": "15 Rue Didouche Mourad Alger centre",
            'nom_personne': self.personne_a_contacter.nom,
            'prenom_personne': self.personne_a_contacter.prenom,
            'telephone_personne': self.personne_a_contacter.telephone
        }

        # URL de l'API pour créer un DPI
        self.url = reverse('creerdpi')  # Assurez-vous que l'URL correspond à la vôtre

        # Client API pour simuler une requête
        self.client = APIClient()

    def test_create_dpi(self):
        response = self.client.post(self.url, {'data': self.patient_data}, format='json')

        # Vérification du statut de la réponse (attend une réussite 200)
        self.assertEqual(response.status_code, 200)

        # Vérification que le DPI a bien été créé
        self.assertTrue(DPI.objects.filter(patient__nom='Kimouche', patient__prenom='Yasmine').exists())

        # Vérification que la réponse contient les données appropriées
        response_data = response.json()
        self.assertEqual(response_data['message'], 'DPI créé avec succès')
        self.assertEqual(response_data['data']['nom'], 'Kimouche')
        self.assertEqual(response_data['data']['prenom'], 'Yasmine')

class TestGetDpi(APITestCase):
    def setUp(self):
        # Création de la personne à contacter
        self.personne_a_contacter = PersonneAContacter.objects.create(
            nom="Sennane", prenom="Rayane", telephone="0000111122"
        )
        self.user = CustomUser.objects.create(
            id=1, username ='felkir', password='felkir1234567891011', role='Patient'
        )
        # Création d'un patient avec les données fournies
        self.patient = Patient.objects.create(
            user = self.user,
            nom="Felkir", 
            prenom="Ryma", 
            date_de_naissance="2004-1-1", 
            telephone="0123456789", 
            nss="1234567891011", 
            mutuelle="Mutuelle", 
            adresse="15 Rue Didouche Mourad Alger centre",
            personne_a_contacter = self.personne_a_contacter
        )
        
        # Création du DPI associé au patient
        self.dpi = DPI.objects.create(patient=self.patient)
        self.url = reverse('dpi')
        
        # Client de test pour faire des requêtes
        self.client = APIClient()


    def test_get_dpi_success(self):
        # Envoi d'une requête GET avec un NSS existant
        response = self.client.get(self.url, {'nss': '1234567891011'})

        # Vérification de la réponse
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Vérification que les données renvoyées incluent toutes les informations
        self.assertEqual(response.data['patient']['nss'], '1234567891011')
        self.assertEqual(response.data['patient']['nom'], 'Felkir')
        self.assertEqual(response.data['patient']['prenom'], 'Ryma')
        self.assertEqual(response.data['patient']['date_de_naissance'], '2004-01-01')
        self.assertEqual(response.data['patient']['telephone'], '0123456789')
        self.assertEqual(response.data['patient']['mutuelle'], 'Mutuelle')
        self.assertEqual(response.data['patient']['adresse'], '15 Rue Didouche Mourad Alger centre')

    def test_get_dpi_not_found(self):
        # Envoi d'une requête GET avec un NSS qui n'existe pas
        response = self.client.get(self.url, {'nss': '00000000000000'})

        # Vérification de la réponse d'erreur
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Aucun DPI trouvé pour ce NSS."})

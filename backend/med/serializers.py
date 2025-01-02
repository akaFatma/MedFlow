from .models import DPI, Patient, PersonneAContacter, Medecin
from rest_framework import serializers

class MedecinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medecin
        fields = ['nom', 'prenom','specialite'] 

class PersonneAContacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonneAContacter
        fields = ['nom', 'prenom','telephone'] 

class PatientSerializer(serializers.ModelSerializer):
    personne_a_contacter = PersonneAContacterSerializer()
    class Meta:
        model = Patient
        fields = ['nom', 'prenom','nss', 'adresse', 'date_de_naissance', 'telephone', 'mutuelle', 'personne_a_contacter']   


class DPISerializer(serializers.ModelSerializer):
    class Meta:
        model = DPI
        fields = '__all__'

class PatientMinimalSerializer(serializers.ModelSerializer):
    etat = serializers.CharField(source='dossier_patient.etat')
    class Meta:
        model = Patient
        fields = ['nom', 'prenom', 'nss', 'etat']        

class DPISerializerGET(serializers.ModelSerializer):
    patient = PatientSerializer()
    class Meta:
        model = DPI
        fields = ['patient','etat']

from rest_framework import serializers
from .models import DPI, Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['nom', 'prenom', 'date_de_naissance', 'adresse', 'telephone', 'nss'] 

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
        fields = ['patient', 'antecedants_medicaux', 'etat']

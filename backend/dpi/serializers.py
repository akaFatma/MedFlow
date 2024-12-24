from rest_framework import serializers
from .models import DPI, Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['nom', 'prenom', 'date_de_naissance', 'adresse', 'telephone', 'nss'] 

class PatientMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['nss', 'nom', 'prenom']        

class DPISerializer(serializers.ModelSerializer):
    class Meta:
        model = DPI
        fields = '__all__'

class DPISerializerGET(serializers.ModelSerializer):
    patient = PatientSerializer()
    class Meta:
        model = DPI
        fields = ['patient', 'antecedants_medicaux']

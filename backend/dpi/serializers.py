from rest_framework import serializers
from .models import DPI
from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['nss', 'nom']  
        
class DPISerializer(serializers.ModelSerializer):
    patient = PatientSerializer()  # Ajouter les informations du patient

    class Meta:
        model = DPI
        fields = ['patient', 'antecedants_medicaux']

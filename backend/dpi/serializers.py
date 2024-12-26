from rest_framework import serializers
from .models import DPI, Patient, Ordonnance, Traitement, Distribution

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

class TraitementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traitement
        fields = ['id', 'nom', 'dose', 'consommation', 'frequence']
class OrdonnanceSerializer(serializers.ModelSerializer):
    traitements = TraitementSerializer(many=True, read_only=True)

    class Meta:
        model = Ordonnance
        fields = ['id', 'validee', 'date_emission', 'traitements']

class DistributionSerializer(serializers.ModelSerializer):
    traitement = TraitementSerializer(read_only=True)
    ordonnance = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Distribution
        fields = ['id', 'ordonnance', 'traitement', 'quantite', 'date_distribution']


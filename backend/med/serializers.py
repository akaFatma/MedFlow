from .models import DPI, Patient, PersonneAContacter, Medecin, Soin, Consultation, Ordonnance,BilanBiologique, BilanRadiologique, Traitement, Distribution
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


class MedecinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medecin
        fields = ['user', 'specialite']

class SoinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Soin
        fields = [ 'etat', 'medicament', 'autre', 'date', 'dpi']

class ConsultationMinimalSerializer(serializers.ModelSerializer):
    medecin_first_name = serializers.CharField(source='medecin.user.first_name', read_only=True)
    medecin_last_name = serializers.CharField(source='medecin.user.last_name', read_only=True)
    medecin_specialite = serializers.CharField(source='medecin.specialite', read_only=True)

    class Meta:
        model = Consultation
        fields = ['id', 'date', 'medecin_first_name', 'medecin_last_name', 'medecin_specialite']

class TraitementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traitement
        fields = ['id', 'nom', 'dose', 'consommation']
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

class BiologiqueSerializer(serializers.ModelSerializer):
    nom = serializers.SerializerMethodField()
    prenom = serializers.SerializerMethodField()
    etat = serializers.SerializerMethodField()

    class Meta:
        model = BilanBiologique
        fields = ['prescription', 'id', 'resultat', 'date_emission', 'nom', 'prenom', 'etat']

    def get_nom(self, obj):
        # Accéder à nom via les relations : consultation -> dpi -> patient -> nom
        return obj.consultation.dpi.patient.nom if obj.consultation and obj.consultation.dpi and obj.consultation.dpi.patient else None

    def get_prenom(self, obj):
        # Accéder à prenom via les relations : consultation -> dpi -> patient -> prenom
        return obj.consultation.dpi.patient.prenom if obj.consultation and obj.consultation.dpi and obj.consultation.dpi.patient else None

    def get_etat(self, obj):
        # Renvoie 'en attente' si resultat est vide, sinon 'fait'
        return 'en attente' if not obj.resultat else 'fait'

class RadiologiqueSerializer(serializers.ModelSerializer):
    nom = serializers.SerializerMethodField()
    prenom = serializers.SerializerMethodField()
    etat = serializers.SerializerMethodField()

    class Meta:
        model = BilanRadiologique
        fields = ['prescription', 'id', 'compte_rendu', 'date_emission', 'nom', 'prenom', 'etat']

    def get_nom(self, obj):
        # Accéder à nom via les relations : consultation -> dpi -> patient -> nom
        return obj.consultation.dpi.patient.nom if obj.consultation and obj.consultation.dpi and obj.consultation.dpi.patient else None

    def get_prenom(self, obj):
        # Accéder à prenom via les relations : consultation -> dpi -> patient -> prenom
        return obj.consultation.dpi.patient.prenom if obj.consultation and obj.consultation.dpi and obj.consultation.dpi.patient else None

    def get_etat(self, obj):
        # Renvoie 'en attente' si resultat est vide, sinon 'fait'
        return 'en attente' if not obj.compte_rendu else 'fait'

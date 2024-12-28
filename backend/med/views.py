import json
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Patient, PersonneAContacter, DPI   
from .serializers import PatientSerializer, PatientMinimalSerializer
from users.decorators import role_required

@api_view(['GET'])
@role_required(allowed_roles=["Médecin"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_patients(request):
    patients = Patient.objects.all()
    serializer = PatientMinimalSerializer(patients, many=True) 
    return Response(serializer.data, status=200)

@api_view(['GET'])
def list_patients_filtered(request):
    nss = request.query_params.get('nss', None)
    if nss:
        patients = Patient.objects.filter(nss=nss) 
    else:
        patients = Patient.objects.all() 
    serializer = PatientMinimalSerializer(patients, many=True)
    return Response(serializer.data, status=200)

from .models import DPI
from .serializers import DPISerializer, DPISerializerGET

@api_view(['GET'])
def get_dpi(request):
    try:
        nss = request.query_params.get('nss')
        dpi = DPI.objects.get(patient__nss=nss)  
        serializer = DPISerializerGET(dpi)
        print(serializer.data)
        return Response(serializer.data, status=200)
    except DPI.DoesNotExist:
        return Response({"error": "Aucun DPI trouvé pour ce NSS."}, status=404)
    
'''
from .utils import generate_qrcode

@api_view(["GET"])
def qr_code(request): 
    pat = Patient.objects.get(nss="123456789")
    path = generate_qrcode(pat)
    print(path)
    return Response({"qrcode": "good"}, status=200)
'''   

from pyzbar.pyzbar import decode
from PIL import Image
import base64
from django.core.files.base import ContentFile

@api_view(['GET'])
def get_dpi_by_qr(request): 
    #lors des tests je n'ai pas pu envoyer un fichier par postman (l'image du qr code scanné), 
    # je l'ai donc encodé, le fichier MedFlow\qrcode_encoder.py fait l'encodage du qr code
    encoded_qr = request.data.get('qrcode')
    if not encoded_qr:
        return Response({"error": "No QR code provided."}, status=400)
    # Decodage
    qr_data = base64.b64decode(encoded_qr)
    temp_file = ContentFile(qr_data, name="temp_qr_code.png")
   
    # Ouvrir l'image et décoder le QR code
    img = Image.open(temp_file)
    decoded_data = decode(img)
    if not decoded_data:
        return Response({"error": "Aucun QR code valide trouvé dans l'image."}, status=400)
    
    # Extraire le NSS à partir des données du QR code
    qr_content = decoded_data[0].data.decode('utf-8')
    
    if not qr_content.startswith("nss:"):
        return Response({"error": "QR code invalide."}, status=400)
    
    nss = qr_content.split(":")[1]  # Récupérer le nss à partir du QR code
    # Rechercher le DPI à partir du nss
    try:
        dpi = DPI.objects.get(patient__nss=nss) 
        serializer = DPISerializerGET(dpi)
        return Response(serializer.data, status=200)
    except DPI.DoesNotExist:
        return Response({"error": "Aucun DPI trouvé pour ce NSS."}, status=404)
    
'''
@api_view(['GET'])
def get_dpi_by_qr_code(request):
    #Methode alternative de la recherche par code qr, à utilisé si possible d'envoyer le fichier entier
    try:
        # Récupérer le fichier QR code depuis la requête
        qr_code_file = request.FILES.get('qr_code')
        if not qr_code_file:
            return Response({"error": "Aucun fichier QR code fourni."}, status=400)

        # Ouvrir l'image QR code et décoder son contenu
        qr_code_image = Image.open(qr_code_file)
        decoded_data = decode(qr_code_image)

        if not decoded_data:
            return Response({"error": "Impossible de décoder le QR code."}, status=400)

        # Extraire les données du QR code (par exemple le NSS)
        qr_content = decoded_data[0].data.decode('utf-8')
        nss = qr_content  # Assumer que le NSS est directement dans le contenu du QR code

        # Rechercher le DPI associé
        dpi = DPI.objects.get(patient__nss=nss)

        # Sérialiser et retourner les données
        serializer = DPISerializerGET(dpi)
        return Response(serializer.data, status=200)

    except DPI.DoesNotExist:
        return Response({"error": "Aucun DPI trouvé pour ce NSS."}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
'''

@csrf_exempt
def rediger_ordonnance(request):
    if request.method == 'POST':
        try:
            print(request.body)  
            body = json.loads(request.body)
            data = body.get('data')

            if not data:
                return JsonResponse({'error': 'Aucune donnée fournie'}, status=400)

            traitements = data.get('traitements')
            if not traitements or not isinstance(traitements, list):
                return JsonResponse({'error': 'Aucun traitement fourni ou format invalide'}, status=400)

            traitements_list = []
            for traitement_data in traitements:
                nom_traitement = traitement_data.get('nom')
                dose = traitement_data.get('dose')
                consommation = traitement_data.get('consommation')
                frequence = traitement_data.get('frequence')

                if not all([nom_traitement, dose, consommation, frequence]):
                    return JsonResponse({'error': 'Certains champs sont manquants pour un traitement'}, status=400)

                traitement = Traitement.objects.create(
                    nom=nom_traitement, dose=dose, consommation=consommation, frequence=frequence
                )
                traitements_list.append(traitement)

            return JsonResponse({'message': 'Traitements enregistrés avec succès', 'traitements': [str(t) for t in traitements_list]})
        except Exception as e:
            print(f"Erreur : {e}")
            return JsonResponse({'error': 'Erreur lors du traitement des données'}, status=400)

    return JsonResponse({'error': 'Requête invalide'}, status=400)

# @csrf_exempt
# # @check_roles(['medecin'])
# def rediger_bilan_biologique(request):
#     if request.method == 'POST':
#         try:
#             print(request.body)  # Ajoutez cette ligne pour voir le contenu brut de la requête
#             body = json.loads(request.body)
#             data = body.get('data')
         
#             prescription = data.get('prescription')
            

#             if not prescription:
#                 return JsonResponse({'error': 'Aucune prescription fournie'}, status=400)

#             return JsonResponse({'message': 'Prescription enregistrée avec succès', 'prescription': prescription})
#         except Exception as e:
#             print(f"Erreur : {e}")
#             return JsonResponse({'error': 'Erreur lors du traitement des données'}, status=400)

#     return JsonResponse({'error': 'Requête invalide'}, status=400)


@csrf_exempt
def creerr_dpi(request): 
    if request.method == 'POST':
        try:
            # Décodage des données envoyées en JSON dans le corps de la requête
            body = json.loads(request.body)
            print(f"Données reçues nomjour : {body}")  # Affiche les données JSON dans la console pour débogage
            data = body.get('data')

            if not data:
                return JsonResponse({'error': 'Aucune donnée fournie'}, status=400)

            # Récupération des valeurs des données
            nom = data.get('nom')
            prenom = data.get('prenom')
            date_naissance = data.get('date_naissance')
            telephone = data.get('telephone')
            nss = data.get('nss')
            mutuelle = data.get('mutuelle')
            adr = data.get('adr')
            nom_personne = data.get('nom_personne')
            prenom_personne = data.get('prenom_personne')
            telephone_personne = data.get('telephone_personne')

            # Validation des champs obligatoires
            if not all([nom, prenom, date_naissance, telephone, adr, nss, mutuelle, nom_personne, prenom_personne, telephone_personne]):
                return JsonResponse({'error': 'Certains champs sont manquants'}, status=400)

            # Création de la personne à contacter
            personne_a_contacter, created = PersonneAContacter.objects.get_or_create(
                nom=nom_personne,
                prenom=prenom_personne,
                telephone=telephone_personne
            )

            # Création du patient
            patient = Patient.objects.create(
                nom=nom, prenom=prenom, date_de_naissance=date_naissance,
                adresse=adr, telephone=telephone, nss=nss, mutuelle=mutuelle,
                personne_a_contacter=personne_a_contacter
            )

            # Création du DPI (Dossier Patient Informatisé)
            dpi = DPI.objects.create(patient=patient)

            # Réponse réussie avec les données créées
            return JsonResponse({
                'message': 'DPI créé avec succès',
                'data': {
                    'nom': nom,
                    'prenom': prenom,
                    'date_naissance': date_naissance,
                    'telephone': telephone,
                    'adresse': adr,
                    'nss': nss,
                    'mutuelle': mutuelle,
                    'personne_nom': nom_personne,
                    'personne_prenom': prenom_personne,
                    'telephone_personne': telephone_personne
                }
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Données JSON invalides'}, status=400)

        except Exception as e:
            print(f"Erreur : {e}")
            return JsonResponse({'error': f'Erreur lors du traitement des données: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Requête invalide'}, status=400)


@csrf_exempt
# @check_roles(['medecin'])
def rediger_ordonnance(request):
    if request.method == 'POST':
        try:
            print(request.body)  # Ajoutez cette ligne pour voir le contenu brut de la requête
            body = json.loads(request.body)
            data = body.get('data')

            if not data:
                return JsonResponse({'error': 'Aucune donnée fournie'}, status=400)

            traitements = data.get('traitements')
            if not traitements or not isinstance(traitements, list):
                return JsonResponse({'error': 'Aucun traitement fourni ou format invalide'}, status=400)

            traitements_list = []
            for traitement_data in traitements:
                nom_traitement = traitement_data.get('nom')
                dose = traitement_data.get('dose')
                consommation = traitement_data.get('consommation')
                frequence = traitement_data.get('frequence')

                if not all([nom_traitement, dose, consommation, frequence]):
                    return JsonResponse({'error': 'Certains champs sont manquants pour un traitement'}, status=400)

                traitement = Traitement.objects.create(
                    nom=nom_traitement, dose=dose, consommation=consommation, frequence=frequence
                )
                traitements_list.append(traitement)

            return JsonResponse({'message': 'Traitements enregistrés avec succès', 'traitements': [str(t) for t in traitements_list]})
        except Exception as e:
            print(f"Erreur : {e}")
            return JsonResponse({'error': 'Erreur lors du traitement des données'}, status=400)

    return JsonResponse({'error': 'Requête invalide'}, status=400)
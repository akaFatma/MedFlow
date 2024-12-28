from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Patient
from .serializers import PatientSerializer, PatientMinimalSerializer
from users.decorators import role_required

@api_view(['GET'])
@role_required(allowed_roles=["Médecin"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_patients(request):
    patients = Patient.objects.all()[:7]
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
    

@api_view(['POST']) 
def create_patient_with_dpi(request): #utilisée pour le test uniquement
    patient_data = request.data.get('patient')
    dpi_data = request.data.get('dpi')

    if not patient_data:
        return Response({"error": "Les données du patient sont manquantes."}, status=400)

    patient_serializer = PatientSerializer(data=patient_data)
    if patient_serializer.is_valid():
        patient = patient_serializer.save()

        if dpi_data:
            dpi_data['patient'] = patient.id
            dpi_serializer = DPISerializer(data=dpi_data)

            if dpi_serializer.is_valid():
                dpi_serializer.save()
                return Response(
                    {"patient": patient_serializer.data, "dpi": dpi_serializer.data},
                    status=201
                )
            else:
                return Response(dpi_serializer.errors, status=400)
            
        return Response(
            {"patient": patient_serializer.data, "dpi": None},
            status=201
        )
    else:
        return Response(patient_serializer.errors, status=400)
    
from .utils import generate_qrcode

@api_view(["GET"])
def qr_code(request): #pour generer le code qr, à revoir 
    pat = Patient.objects.get(nss="123456789")
    path = generate_qrcode(pat)
    print(path)
    return Response({"qrcode": "good"}, status=200)

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



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Patient
from .serializers import PatientSerializer

@api_view(['GET'])
def list_patients(request):
    search_nss = request.data.get('nss')  # Récupérer le paramètre "nss" si présent
    patients = Patient.objects.all()

    if search_nss:
        patients = patients.filter(nss__startswith=search_nss)  # Filtrer par NSS (partiel ou complet)

    # Pagination
    paginator = PageNumberPagination()
    paginator.page_size = 10  # Nombre de résultats par page
    paginated_patients = paginator.paginate_queryset(patients, request)

    serializer = PatientSerializer(paginated_patients, many=True)
    return paginator.get_paginated_response(serializer.data)

from .models import DPI
from .serializers import DPISerializer

@api_view(['GET'])
def get_dpi(request, nss):
    try:
        dpi = DPI.objects.get(patient__nss=nss)  # Rechercher le DPI lié au patient par NSS
        serializer = DPISerializer(dpi)
        return Response(serializer.data, status=200)
    except DPI.DoesNotExist:
        return Response({"error": "Aucun DPI trouvé pour ce NSS."}, status=404)

'''
@api_view(['GET'])
def create_patient_with_dpi(request):
    print("hi")
    return Response({"hi" : "bitch"}, status=200)

'''

@api_view(['POST'])
def create_patient_with_dpi(request):
    # Récupérer les données du corps de la requête
    patient_data = request.data.get('patient')
    dpi_data = request.data.get('dpi')

    # Vérifier si les données du patient sont fournies
    if not patient_data:
        return Response({"error": "Les données du patient sont manquantes."}, status=400)

    # Sérialiser les données du patient
    patient_serializer = PatientSerializer(data=patient_data)
    if patient_serializer.is_valid():
        # Sauvegarder le patient
        patient = patient_serializer.save()

        # Vérifier si les données du DPI sont fournies
        if dpi_data:
            # Ajouter une référence au patient dans les données du DPI
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

        # Si aucun DPI n'est fourni, retourner uniquement le patient
        return Response(
            {"patient": patient_serializer.data, "dpi": None},
            status=201
        )
    else:
        return Response(patient_serializer.errors, status=400)
    
from .utils import generate_qrcode

@api_view(["GET"])
def qr_code(request): 
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
    encoded_qr = request.data.get('qr_code')
    if not encoded_qr:
        return Response({"error": "No QR code provided."}, status=400)
        
        # Decode the Base64 string
    qr_data = base64.b64decode(encoded_qr)
        
        # Save the decoded file temporarily
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
        dpi = DPI.objects.get(patient__nss=nss)  # Rechercher le DPI lié au patient par NSS
        serializer = DPISerializer(dpi)
        return Response(serializer.data, status=200)
    except DPI.DoesNotExist:
        return Response({"error": "Aucun DPI trouvé pour ce NSS."}, status=404)
    
'''
@api_view(['GET'])
def get_dpi_by_qr_code(request):
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
        from .models import DPI
        dpi = DPI.objects.get(patient__nss=nss)

        # Sérialiser et retourner les données
        from .serializers import DPISerializer
        serializer = DPISerializer(dpi)
        return Response(serializer.data, status=200)

    except DPI.DoesNotExist:
        return Response({"error": "Aucun DPI trouvé pour ce NSS."}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
'''
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Patient 
from .serializers import PatientSerializer, PatientMinimalSerializer

@api_view(['GET'])
def list_patients(request):
    search_nss = request.data.get('nss')
    patients = Patient.objects.all()

    if search_nss:
        patients = patients.filter(nss__startswith=search_nss)  # Recuperer tous les dpi qui commence par le search_nss

    # Pagination, apparemment c'est pour ne pas envoyer tous les patients s'ils sont nombreux
    # z3ma kima insta myb3tolkch kamel l existing posts mais une page, dk if it's helpful
    # ila khdma zayda 9ololi na7ih, n7bes f patients ndir return patients --malak

    paginator = PageNumberPagination()
    paginator.page_size = 10  # Nombre de résultats par page
    paginated_patients = paginator.paginate_queryset(patients, request)

    serializer = PatientMinimalSerializer(paginated_patients, many=True)
    return paginator.get_paginated_response(serializer.data)

from .models import DPI
from .serializers import DPISerializer, DPISerializerGET

@api_view(['GET'])
def get_dpi(request, nss):
    try:
        dpi = DPI.objects.get(patient__nss=nss)  # Rechercher le DPI lié au patient par NSS
        serializer = DPISerializerGET(dpi)
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

from .models import Ordonnance, Traitement, Distribution
from .serializers import DistributionSerializer, OrdonnanceSerializer

@api_view(['GET'])
def envoyer_ordonnance_sgph(request, id):
    try:
        ordonnance = Ordonnance.objects.get(id=id)
        serializer = OrdonnanceSerializer(ordonnance)
        return Response(serializer.data, status=200)
    except Ordonnance.DoesNotExist:
        return Response({"error": "Ordonnance introuvable"}, status=404)

@api_view(['POST'])
def valider_ordonnance(request):
    ordonnance_id = request.data.get("ordonnance_id")
    if not ordonnance_id:
        return Response({"error": "L'ID de l'ordonnance est requis."}, status=400)

    try:
        ordonnance = Ordonnance.objects.get(id=ordonnance_id)
    except Ordonnance.DoesNotExist:
        return Response({"error": "Ordonnance introuvable."}, status=404)

    ordonnance.validee = True
    ordonnance.save()

    return Response({
        "message": "Ordonnance validée avec succès.",
        "ordonnance_id": ordonnance.id,
        "status": ordonnance.validee
    }, status=200)

@api_view(['POST'])
def valider_ordonnance(request, id):
    ordonnance = Ordonnance.objects.get(id=id)
    if not ordonnance:
        return Response({'error': 'Ordonnance introuvable'}, status=404)
    
    if ordonnance.validee:
        return Response({'message': 'Ordonnance déjà validée'}, status=400)

    sgph_response = request.data.get('validation') 
    ordonnance.validee = sgph_response
    ordonnance.save()

    status_message = 'validée' if sgph_response else 'non validée'
    return Response({'message': f"Ordonnance {status_message}"}, status=200)

@api_view(['POST'])
def distribuer_medicament(request):
    ordonnance_id = request.data.get('ordonnance_id')
    traitement_id = request.data.get('traitement_id')
    quantite = request.data.get('quantite')

    ordonnance = Ordonnance.objects.filter(id=ordonnance_id).first()
    if not ordonnance or not ordonnance.validee:
        return Response({'error': 'Ordonnance invalide ou non validée'}, status=400)

    traitement = Traitement.objects.filter(id=traitement_id).first()
    if not traitement:
        return Response({'error': 'Traitement introuvable'}, status=404)

    distribution = Distribution.objects.create(
        ordonnance=ordonnance,
        traitement=traitement,
        quantite=quantite
    )

    serializer = DistributionSerializer(distribution)
    return Response(serializer.data, status=201)

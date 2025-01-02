import json
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import (
    Patient, PersonneAContacter, DPI,
    Consultation,
    BilanBiologique,  
    BilanRadiologique, 
    Ordonnance,
    Soin,
    Examen,
    Traitement   )
from .serializers import PatientSerializer, PatientMinimalSerializer
from users.decorators import role_required
from users.serializers import UserSerializer
from .utils import generate_qrcode

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def list_patients(request):
    patients = Patient.objects.all()
    serializer = PatientMinimalSerializer(patients, many=True) 
    return Response(serializer.data, status=200)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
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
@authentication_classes([SessionAuthentication, TokenAuthentication])
def get_dpi(request):
    try:
        nss = request.query_params.get('nss')
        dpi = DPI.objects.get(patient__nss=nss) 
        serializer = DPISerializerGET(dpi)
        print(serializer.data)
        return Response(serializer.data, status=200)
    except DPI.DoesNotExist:
        return Response({"error": "Aucun DPI trouvé pour ce NSS."}, status=404)
    

@csrf_exempt
def creer_dpi(request): 
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
            # Create the user (signup logic)
            user_data = {
                'username': nom+prenom,
                'password': nom+nss,
                'first_name': nom,
                'last_name': prenom,
                'role': 'Patient'
            }
            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid():
                user = user_serializer.save()    


            # Création du patient
                patient = Patient.objects.create(
                    user = user,
                    nom=nom, prenom=prenom, date_de_naissance=date_naissance,
                    adresse=adr, telephone=telephone, nss=nss, mutuelle=mutuelle,
                    personne_a_contacter=personne_a_contacter
                )
                generate_qrcode(patient)
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


# Rédaction d'ordonnance - Traitements
@csrf_exempt
# @check_roles(['medecin'])
def rediger_ordonnance(request):
    if request.method == 'POST':
        try:
            print(request.body)  # Affiche le contenu brut de la requête pour déboguer
            body = json.loads(request.body)
            data = body.get('data')

            if not data:
                return JsonResponse({'error': 'Aucune donnée fournie'}, status=400)

            nss = data.get('nss')
            if not nss:
                return JsonResponse({'error': 'Numéro de sécurité sociale (NSS) requis'}, status=400)

            # Recherche le DPI correspondant au NSS
            try:
                dpi = DPI.objects.get(patient__nss=nss)
            except DPI.DoesNotExist:
                return JsonResponse({'error': 'Aucun DPI trouvé pour ce NSS'}, status=404)

            # Recherche la dernière consultation d'aujourd'hui pour ce DPI
            date = now()
            consultation = Consultation.objects.filter(dpi=dpi, date__date=date.date()).order_by('-date').first()

            if not consultation:
                return JsonResponse({'error': 'Aucune consultation trouvée pour ce DPI aujourd\'hui'}, status=404)

            # Récupère les traitements de la requête
            traitements = data.get('traitements')
            if not traitements or not isinstance(traitements, list):
                return JsonResponse({'error': 'Aucun traitement fourni ou format invalide'}, status=400)

            # Crée les objets Traitement
            traitements_list = []
            for traitement_data in traitements:
                nom_traitement = traitement_data.get('nom')
                dose = traitement_data.get('dose')
                consommation = traitement_data.get('consommation')

                if not all([nom_traitement, dose, consommation]):
                    return JsonResponse({'error': 'Certains champs sont manquants pour un traitement'}, status=400)

                traitement = Traitement.objects.create(
                    nom=nom_traitement,
                    dose=dose,
                    consommation=consommation,
                )
                traitements_list.append(traitement)

            # Crée une ordonnance et l'affecte à la consultation
            ordonnance = Ordonnance.objects.create(
                patient=dpi.patient,  # Associe la bonne relation patient
                status='en_attente'
            )
            ordonnance.traitements.set(traitements_list)  # Ajoute les traitements à l'ordonnance
            ordonnance.save()

            # Associe l'ordonnance à la consultation
            consultation.ordonnance = ordonnance
            consultation.save()

            return JsonResponse({
                'message': 'Ordonnance créée et associée avec succès',
                'ordonnance': {
                    'id': ordonnance.id,
                    'date_emission': ordonnance.date_emission,
                    'status': ordonnance.status,
                    'traitements': [str(t) for t in traitements_list]
                }
            })
        except Exception as e:
            print(f"Erreur : {e}")
            return JsonResponse({'error': 'Erreur lors du traitement des données'}, status=400)

    return JsonResponse({'error': 'Requête invalide'}, status=400)

# @csrf_exempt
# # @check_roles(['medecin'])
@csrf_exempt
def rediger_bilan_radiologique(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            data = body.get('data')
            nss = data.get('nss')
            if not nss:
                return JsonResponse({'error': 'NSS requis'}, status=400)
            try:
                dpi = DPI.objects.get(patient__nss=nss)
            except DPI.DoesNotExist:
                return JsonResponse({'error': 'Aucun DPI trouvé'}, status=404)
            date = now()
            consultation = Consultation.objects.filter(dpi=dpi, date__date=date.date()).order_by('-date').first()
            if not consultation:
                return JsonResponse({'error': 'Aucune consultation trouvée aujourd\'hui'}, status=404)
            prescription = data.get('prescription')
            if not prescription  :
                return JsonResponse({'error': 'Prescription ou compte-rendu manquant'}, status=400)
            bilan = BilanRadiologique.objects.create(
                consultation=consultation,
                prescription=prescription,
                date_emission=date,
                compte_rendu=None,
                image_url=None
            )
            return JsonResponse({
                'message': 'Bilan radiologique enregistré avec succès',
                'bilan_id': bilan.id,
                'consultation_id': consultation.id
            })
        except Exception as e:
            return JsonResponse({'error': 'Erreur lors du traitement des données'}, status=400)
    return JsonResponse({'error': 'Requête invalide'}, status=400)

@csrf_exempt
def rediger_bilan_biologique(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            data = body.get('data')
            nss = data.get('nss')
            if not nss:
                return JsonResponse({'error': 'NSS requis'}, status=400)
            try:
                dpi = DPI.objects.get(patient__nss=nss)
            except DPI.DoesNotExist:
                return JsonResponse({'error': 'Aucun DPI trouvé'}, status=404)
            date = now()
            consultation = Consultation.objects.filter(dpi=dpi, date__date=date.date()).order_by('-date').first()
            if not consultation:
                return JsonResponse({'error': 'Aucune consultation trouvée aujourd\'hui'}, status=404)
            prescription = data.get('prescription')
            resultat = None
            if not prescription :
                return JsonResponse({'error': 'Prescription ou compte-rendu manquant'}, status=400)
            bilan = BilanRadiologique.objects.create(
                consultation=consultation,
                prescription=prescription,
                date_emission=date,
                resultat=resultat,
            )
            return JsonResponse({
                'message': 'Bilan radiologique enregistré avec succès',
                'bilan_id': bilan.id,
                'consultation_id': consultation.id
            })
        except Exception as e:
            return JsonResponse({'error': 'Erreur lors du traitement des données'}, status=400)
    return JsonResponse({'error': 'Requête invalide'}, status=400)

@csrf_exempt
def rediger_soin(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            nss = body.get('nss')
            if not nss:
                return JsonResponse({'error': 'NSS requis'}, status=400)
            try:
                dpi = DPI.objects.get(patient__nss=nss)
            except DPI.DoesNotExist:
                return JsonResponse({'error': 'Aucun DPI trouvé'}, status=404)
            etat = body.get('etat')
            medicament = body.get('medicament')
            autre = body.get('autre')
            if not etat or not medicament or not autre:
                return JsonResponse({'error': 'Etat, médicament ou autre information manquants'}, status=400)
            soin = Soin.objects.create(
                etat=etat,
                medicament=medicament,
                autre=autre,
                dpi=dpi,
                date=now()
            )
            dpi.soins.add(soin)  # Associer le soin au DPI
            return JsonResponse({
                'message': 'Soin enregistré avec succès',
                'soin_id': soin.id,
                'dpi_id': dpi.id
            })
        except Exception as e:
            return JsonResponse({'error': f'Erreur lors du traitement des données: {str(e)}'}, status=400)
    return JsonResponse({'error': 'Requête invalide'}, status=400)

@csrf_exempt
def commencer_consultation(request):
    if request.method == 'POST':
        try:
            # Afficher le corps de la requête
            print("Request Body:", request.body)
            
            body = json.loads(request.body)

            # Log des données reçues
            print("body received:", body)

            # Validation du NSS
            nss = body.get('nss')
            if not nss:
                return JsonResponse({'error': 'NSS requis'}, status=400)
            
            print(f"NSS reçu: {nss}")

            try:
                dpi = DPI.objects.get(patient__nss=nss)
                print(f"DPI trouvé: {dpi}")
            except DPI.DoesNotExist:
                return JsonResponse({'error': 'Aucun DPI trouvé'}, status=404)

            # Création de la consultation
            consultation = Consultation.objects.create(
                dpi=dpi,
                resume="",  
                ordonnance=None,
                date=now()  
            )
            print(f"Consultation créée avec ID: {consultation.id}")
            
            ordonnance = Ordonnance.objects.create(
                consultation=consultation,  # Associe l'ordonnance à la consultation
                status='en_attente'
            )
            print(f"Ordonnance créée avec ID: {ordonnance.id}")

            # Traitements - Ajout direct
            traitements = body.get('traitements')
            if not traitements or not isinstance(traitements, list):
                return JsonResponse({'error': 'Aucun traitement fourni ou format invalide'}, status=400)
            
            print(f"Traitements reçus: {traitements}")

            for traitement_data in traitements:
                nom_traitement = traitement_data.get('nom')
                dose = traitement_data.get('dose')
                consommation = traitement_data.get('consommation')

                if not all([nom_traitement, dose, consommation]):
                    return JsonResponse({'error': 'Certains champs sont manquants pour un traitement'}, status=400)
                
                print(f"Ajout du traitement: nom={nom_traitement}, dose={dose}, consommation={consommation}")

                traitement = Traitement.objects.create(
                    nom=nom_traitement,
                    dose=dose,
                    consommation=consommation,
                )
                ordonnance.traitements.add(traitement)  # Ajoute directement le traitement à l'ordonnance
                print(f"Traitement ajouté à l'ordonnance: {traitement.id}")

            ordonnance.save()
            consultation.ordonnance = ordonnance

            # Examens - Ajout avec set()
            examens = body.get('examens')
            if examens and isinstance(examens, list):
                created_exams = []
                for exam_data in examens:
                    consigne = exam_data
                    if consigne:
                        # Création de l'examen associé à la consultation
                        exam = Examen.objects.create(
                            consigne=consigne,
                            consultation = consultation  # On associe l'examen à la consultation
                        )
                        is_biologique = bilan_type_detector(consigne)
                        if is_biologique:
                            bilan_bio = BilanBiologique.objects.create(
                                prescription=consigne,
                                consultation=consultation,
                                date_emission=now() ,
                                resultat=''                                
                            )
                        else:
                            bilan_radio = BilanRadiologique.objects.create(
                                prescription=consigne,
                                consultation=consultation,
                                date_emission=now() ,
                                compte_rendu='',
                                image_url=None                               
                            )
                        created_exams.append(exam)
                        print(f"Examen créé: {exam.id} avec consigne: {consigne}")

                # Ajout de tous les examens à la consultation
                consultation.examens.set(created_exams)

            # Mise à jour du résumé de la consultation
            resume = body.get('resume')
            if resume:
                consultation.resume = resume
                print(f"Résumé mis à jour: {resume}")

            consultation.save()  # Sauvegarde de la consultation avec les modifications
            print(f"Consultation sauvegardée avec l'ordonnance et les examens")

            # Retour de la réponse réussie
            return JsonResponse({'message': 'Consultation commencée avec succès'}, status=201)

        except Exception as e:
            print(f"Erreur dans le traitement: {str(e)}")  # Log l'erreur
            return JsonResponse({'error': f'Erreur lors du traitement des données: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Requête invalide'}, status=400)
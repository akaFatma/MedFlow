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
    Patient, PersonneAContacter, DPI, Medecin,
    Consultation,
    BilanBiologique,  
    BilanRadiologique, 
    Ordonnance,
    Soin,
    Examen,
    Traitement, Distribution  )
from .serializers import( PatientSerializer, PatientMinimalSerializer,
                          SoinSerializer, ConsultationMinimalSerializer,
                            DistributionSerializer, OrdonnanceSerializer,
                              BiologiqueSerializer, RadiologiqueSerializer)
from users.decorators import role_required
from users.serializers import UserSerializer
from .utils import generate_qrcode
from django.utils.timezone import now
from rest_framework.exceptions import NotFound
from rest_framework import status
from .models import DPI
from .serializers import DPISerializer, DPISerializerGET
from django.http import FileResponse
from django.conf import settings
import os

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def list_patients(request):
    """
    Liste tous les patients.

    Cette vue retourne une liste minimale des patients existants dans la base de données.

    Retourne :
        - Une réponse JSON contenant la liste des patients sérialisés.
        - Statut HTTP 200 en cas de succès.
    """
    patients = Patient.objects.all()
    serializer = PatientMinimalSerializer(patients, many=True) 
    return Response(serializer.data, status=200)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def list_patients_filtered(request):
    """
    Liste les patients avec un filtre optionnel.

    Cette vue retourne une liste de patients. Si le paramètre `nss` est fourni
    dans les paramètres de requête, seuls les patients correspondant à ce numéro 
    de sécurité sociale (NSS) sont inclus dans la réponse.

    Paramètres de requête :
        - nss (str) : (Optionnel) Le numéro de sécurité sociale pour filtrer les patients.

    Retourne :
        - Une réponse JSON contenant la liste des patients sérialisés (filtrée si `nss` est fourni).
        - Statut HTTP 200 en cas de succès.
    """
    nss = request.query_params.get('nss', None)
    if nss:
        patients = Patient.objects.filter(nss=nss) 
    else:
        patients = Patient.objects.all() 
    serializer = PatientMinimalSerializer(patients, many=True)
    return Response(serializer.data, status=200)




@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def get_dpi(request):
    """
    Récupère le Dossier Patient Informatisé (DPI) d'un patient.

    Cette vue retourne les informations du DPI correspondant au numéro de 
    sécurité sociale (NSS) fourni.

    Paramètres de requête :
        - nss (str) : Le numéro de sécurité sociale du patient pour lequel récupérer le DPI.

    Retourne :
        - Une réponse JSON contenant les données sérialisées du DPI si trouvé.
        - Statut HTTP 200 en cas de succès.
        - Une erreur JSON avec le message "Aucun DPI trouvé pour ce NSS." et un statut HTTP 404 si aucun DPI n'est trouvé.
    """
    try:
        nss = request.query_params.get('nss')
        print('nss ', nss)
        dpi = DPI.objects.get(patient__nss=nss) 
        serializer = DPISerializerGET(dpi)
        # print(serializer.data)
        return Response(serializer.data, status=200)
    except DPI.DoesNotExist:
        return Response({"error": "Aucun DPI trouvé pour ce NSS."}, status=404)

    

@csrf_exempt
@authentication_classes([SessionAuthentication, TokenAuthentication])
def creer_dpi(request):
    """
    Crée un Dossier Patient Informatisé (DPI).

    Cette vue permet de créer un DPI pour un patient à partir des données fournies dans le corps de la requête.

    Méthode :
        - POST

    Données requises dans le corps de la requête (JSON) :
        - nom (str) : Nom du patient.
        - prenom (str) : Prénom du patient.
        - date_naissance (str) : Date de naissance du patient (format YYYY-MM-DD).
        - telephone (str) : Numéro de téléphone du patient.
        - nss (str) : Numéro de sécurité sociale du patient.
        - mutuelle (str) : Nom de la mutuelle du patient.
        - adr (str) : Adresse du patient.
        - nom_personne (str) : Nom de la personne à contacter en cas d'urgence.
        - prenom_personne (str) : Prénom de la personne à contacter en cas d'urgence.
        - telephone_personne (str) : Numéro de téléphone de la personne à contacter.

    Retourne :
        - En cas de succès :
            - Une réponse JSON contenant un message de confirmation et les données créées.
            - Statut HTTP 200.
        - En cas d'erreur :
            - Une réponse JSON avec un message d'erreur et un statut HTTP 400 (erreur de validation ou de données JSON invalides).
            - Une réponse JSON avec un statut HTTP 500 en cas d'erreur serveur.

    Exceptions :
        - json.JSONDecodeError : Si les données JSON envoyées ne sont pas valides.
        - Exception : Si une erreur se produit lors de la création du DPI ou des entités associées.
    """
    if request.method == 'POST':
        try:
            # Décodage des données envoyées en JSON dans le corps de la requête
            body = json.loads(request.body)
            print(f"Données reçues : {body}")  # Affiche les données JSON dans la console pour débogage
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
            # Création de l'utilisateur (logique d'inscription)
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
                    user=user,
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
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Données JSON invalides'}, status=400)

        except Exception as e:
            print(f"Erreur : {e}")
            return JsonResponse({'error': f'Erreur lors du traitement des données: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Requête invalide'}, status=400)



@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def rediger_soin(request):
    """
    Fonction permettant de rédiger un soin pour un patient en utilisant le numéro de sécurité sociale (NSS).
    
    Cette fonction prend une requête POST contenant les informations nécessaires pour créer un soin. 
    Les informations attendues sont le numéro de sécurité sociale (NSS), l'état du patient, 
    le médicament prescrit et toute autre information complémentaire. Le soin sera associé au 
    Dossier Patient Informatique (DPI) du patient correspondant au NSS.

    Retourne un message de succès avec l'identifiant du soin créé et l'identifiant du DPI du patient, 
    ou une erreur si une information est manquante ou si le patient n'est pas trouvé.

    Arguments :
        request : Requête HTTP contenant les données du soin à rédiger.

    Retour :
        JsonResponse : Un message de succès ou d'erreur avec des informations pertinentes.
    """
    try:
        # Charger le corps de la requête
        body = json.loads(request.body)
        nss = body.get('nss')
        
        # Vérifier si le NSS est fourni
        if not nss:
            return JsonResponse({'error': 'NSS requis'}, status=400)
        
        # Tenter de récupérer le DPI du patient à partir du NSS
        try:
            dpi = DPI.objects.get(patient__nss=nss)
        except DPI.DoesNotExist:
            return JsonResponse({'error': 'Aucun DPI trouvé'}, status=404)
        
        # Extraire les autres informations nécessaires
        etat = body.get('etat')
        medicament = body.get('medicament')
        autre = body.get('autre')

        # Vérifier si toutes les informations sont présentes
        if not etat or not medicament or not autre:
            return JsonResponse({'error': 'Etat, médicament ou autre information manquants'}, status=400)

        # Créer un nouveau soin
        soin = Soin.objects.create(
            etat=etat,
            medicament=medicament,
            autre=autre,
            dpi=dpi,
            date=now()
        )
        
        # Associer le soin au DPI
        dpi.soins.add(soin)
        
        # Retourner un message de succès avec les identifiants du soin et du DPI
        return JsonResponse({
            'message': 'Soin enregistré avec succès',
            'soin_id': soin.id,
            'dpi_id': dpi.id
            })
    
    except Exception as e:
        # En cas d'erreur, retourner un message d'erreur avec les détails
        return JsonResponse({'error': f'Erreur lors du traitement des données: {str(e)}'}, status=400)
    
    # Si la requête est invalide
    return JsonResponse({'error': 'Requête invalide'}, status=400)


@csrf_exempt
@authentication_classes([SessionAuthentication, TokenAuthentication])
def commencer_consultation(request):
    """
    Fonction permettant de commencer une consultation pour un patient en utilisant le numéro de sécurité sociale (NSS).
    
    Cette fonction prend une requête POST contenant des informations nécessaires pour créer une consultation médicale. 
    Les informations attendues sont le numéro de sécurité sociale (NSS) du patient, le nom d'utilisateur du médecin, 
    une liste de traitements, des examens, et un résumé de la consultation. La fonction crée une consultation, 
    une ordonnance, ajoute des traitements et des examens associés, puis met à jour la consultation avec un résumé.

    Retourne un message de succès avec les détails de la consultation créée, ou une erreur si des informations sont manquantes
    ou si un problème survient lors de la création de la consultation.

    Arguments :
        request : Requête HTTP contenant les données nécessaires pour commencer la consultation.

    Retour :
        JsonResponse : Un message de succès ou d'erreur avec des informations pertinentes.
    """
    if request.method == 'POST':
        try:
            # Afficher le corps de la requête pour le log
            print("Request Body:", request.body)
            
            # Charger les données reçues
            body = json.loads(request.body)

            # Validation du NSS
            nss = body.get('nss')
            if not nss:
                return JsonResponse({'error': 'NSS requis'}, status=400)
            
            print(f"NSS reçu: {nss}")

            # Tenter de récupérer le DPI du patient à partir du NSS
            try:
                dpi = DPI.objects.get(patient__nss=nss)
                print(f"DPI trouvé: {dpi}")
            except DPI.DoesNotExist:
                return JsonResponse({'error': 'Aucun DPI trouvé'}, status=404)

            # Vérification et récupération du médecin
            username = body.get('username')
            try:
                user = CustomUser.objects.get(username=username)
                medecin = Medecin.objects.get(user=user)
            except CustomUser.DoesNotExist:
                raise NotFound("Utilisateur introuvable avec ce nom d'utilisateur.")
            except Medecin.DoesNotExist:
                raise NotFound("Aucun profil de médecin trouvé pour cet utilisateur.")
            print('Médecin trouvé: ', medecin)

            # Création de la consultation
            consultation = Consultation.objects.create(
                dpi=dpi,
                medecin=medecin,
                resume="",  
                ordonnance=None,
                date=now()  
            )
            print(f"Consultation créée avec ID: {consultation.id}")
            
            # Création de l'ordonnance
            ordonnance = Ordonnance.objects.create(
                dpi = dpi,
                date_emission = now()
            )
            print(f"Ordonnance créée avec ID: {ordonnance.id}")

            # Traitements - Ajout direct
            traitements = body.get('traitements')
            if not traitements or not isinstance(traitements, list):
                return JsonResponse({'error': 'Aucun traitement fourni ou format invalide'}, status=400)
            
            print(f"Traitements reçus: {traitements}")

            # Création des traitements et ajout à l'ordonnance
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
                ordonnance.traitements.add(traitement)  # Ajoute le traitement à l'ordonnance
                print(f"Traitement ajouté à l'ordonnance: {traitement.id}")

            ordonnance.save()
            consultation.ordonnance = ordonnance

            # Examens - Création des examens et ajout à la consultation
            examens = body.get('examens')
            if examens and isinstance(examens, list):
                created_exams = []
                for exam_data in examens:
                    consigne = exam_data
                    if consigne:
                        # Création de l'examen associé à la consultation
                        exam = Examen.objects.create(
                            date_emission = now(),
                            prescription=consigne,
                            consultation = consultation  # Association à la consultation
                        )
                        is_biologique = bilan_type_detector(consigne)
                        if is_biologique:
                            bilan_bio = BilanBiologique.objects.create(
                                idc = consultation.id,
                                prescription=consigne,
                                consultation=consultation,
                                date_emission=now() ,
                                resultat=''                                 
                            )
                        else:
                            bilan_radio = BilanRadiologique.objects.create(
                                idc = consultation.id,
                                prescription=consigne,
                                consultation=consultation,
                                date_emission=now() ,
                                compte_rendu='',
                                image=None                          
                            )
                        created_exams.append(exam)
                        print(f"Examen créé: {exam.id} avec consigne: {consigne}")

                # Ajouter les examens à la consultation
                consultation.examens.set(created_exams)

            # Mise à jour du résumé de la consultation si nécessaire
            resume = body.get('resume')
            if resume:
                consultation.resume = resume
                print(f"Résumé mis à jour: {resume}")

            consultation.save()  # Sauvegarder la consultation après les modifications
            print(f"Consultation sauvegardée avec l'ordonnance et les examens")

            # Retourner un message de succès
            return JsonResponse({'message': 'Consultation commencée avec succès'}, status=201)

        except Exception as e:
            print(f"Erreur dans le traitement: {str(e)}")  # Log l'erreur
            return JsonResponse({'error': f'Erreur lors du traitement des données: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Requête invalide'}, status=400)


from users.models import CustomUser


@api_view(['GET'])
def MedecinView(request):
    """
    Fonction permettant de récupérer les informations d'un médecin en fonction du nom d'utilisateur (username).

    Cette fonction prend une requête GET avec un paramètre 'username' pour récupérer les informations du médecin 
    associé à cet utilisateur, notamment son prénom, nom, et spécialité. Si le médecin ou l'utilisateur n'existe pas,
    une erreur est renvoyée.

    Arguments :
        request : Requête HTTP contenant le paramètre 'username' dans les paramètres GET.

    Retour :
        Response : Un dictionnaire avec les informations du médecin ou un message d'erreur.
    """
    # Récupérer le nom d'utilisateur depuis les paramètres GET
    username = request.GET.get('username') 
    print(username)
    
    # Vérifier si le nom d'utilisateur est fourni
    if not username:
        return Response({"error": "Username is required."}, status=400)
        
    try:
        # Récupérer l'utilisateur à partir du nom d'utilisateur
        user = CustomUser.objects.get(username=username)
        
        # Récupérer le profil de médecin associé à cet utilisateur
        medecin = Medecin.objects.get(user=user)
        
    except CustomUser.DoesNotExist:
        # Si l'utilisateur n'existe pas
        raise NotFound("User with this username does not exist.")
    except Medecin.DoesNotExist:
        # Si aucun profil de médecin n'est trouvé pour cet utilisateur
        raise NotFound("No Medecin profile found for this user.")
        
    # Retourner les informations du médecin
    return Response({
        "first_name": user.first_name,
        "last_name": user.last_name,
        "specialite": medecin.specialite
    })



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def get_patient_consultations(request):
    """
    Fonction permettant de récupérer toutes les consultations d'un patient à partir de son numéro de sécurité sociale (NSS).
    
    Cette fonction prend une requête GET contenant le numéro de sécurité sociale (NSS) du patient et retourne toutes les consultations
    associées au patient correspondant. Si aucun DPI n'est trouvé pour le NSS donné, une erreur est renvoyée.
    
    Arguments :
        request : Requête HTTP contenant le paramètre 'nss' dans les paramètres de la requête GET.
    
    Retour :
        Response : La liste des consultations du patient sous forme de données sérialisées ou un message d'erreur.
    """
    try:
        # Récupérer le NSS depuis les paramètres de la requête
        nss = request.query_params.get('nss')

        # Récupérer le DPI associé au NSS du patient
        dpi = DPI.objects.get(patient__nss=nss)

        # Récupérer toutes les consultations liées à ce DPI
        consultations = Consultation.objects.filter(dpi=dpi)

        # Sérialiser les consultations récupérées
        serializer = ConsultationMinimalSerializer(consultations, many=True)

        # Retourner les consultations sérialisées
        return Response(serializer.data, status=status.HTTP_200_OK)

    except DPI.DoesNotExist:
        # Si aucun DPI n'est trouvé pour le NSS donné
        return Response({'error': 'No DPI found for the given NSS'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        # En cas d'erreur interne du serveur
        return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])  # Attends une requête POST avec l'ID de la consultation dans le corps
@authentication_classes([SessionAuthentication, TokenAuthentication])  # Assure que seul un utilisateur authentifié peut appeler cette fonction
def get_user_info(request):
    """
    Fonction permettant de récupérer les informations liées à une consultation spécifique, 
    y compris les bilans biologiques, radiologiques, traitements, et ordonnance.

    Cette fonction prend une requête POST avec l'ID de la consultation dans le corps de la requête, 
    valide l'ID et récupère les informations associées à la consultation, telles que les bilans, les traitements,
    et les ordonnances liées à cette consultation.

    Arguments :
        request : Requête HTTP contenant l'ID de la consultation dans le corps de la requête (JSON).

    Retour :
        Response : Un dictionnaire contenant les détails de la consultation, les prescriptions des bilans, 
                  les résultats des bilans biologiques, les comptes rendus des bilans radiologiques, 
                  et les informations sur les traitements dans l'ordonnance.
    """
    # Étape 1 : Charger et valider le corps de la requête
    try:
        body = json.loads(request.body)  # Charger les données JSON
        consultation_id = body  # Extraire l'ID de la consultation
        if not consultation_id:
            return Response({'error': 'ID de consultation non fourni.'}, status=400)
    except json.JSONDecodeError:
        return Response({'error': 'Format JSON invalide.'}, status=400)

    # Étape 2 : Récupérer la consultation correspondante
    try:
        consultation = Consultation.objects.get(id=consultation_id)  # Récupérer la consultation via son ID
    except Consultation.DoesNotExist:
        return Response({'error': 'Aucune consultation trouvée pour cet ID.'}, status=404)
    
    # Étape 3 : Construire la réponse
    # Récupérer les bilans biologiques associés à cette consultation
    bilansbiologiques = BilanBiologique.objects.filter(idc=consultation.id)

    # Récupérer les bilans radiologiques associés à cette consultation
    bilansradiologiques = BilanRadiologique.objects.filter(idc=consultation.id) 
    compte_rendus = BilanRadiologique.objects.filter(idc=consultation.id).values_list('compte_rendu', flat=True)
    resultats = BilanBiologique.objects.filter(idc=consultation.id).values_list('resultat', flat=True)
    images = BilanRadiologique.objects.filter(idc=consultation.id).values_list('image', flat=True)
    
    # Récupérer les traitements dans l'ordonnance de la consultation
    ordo = consultation.ordonnance
    noms = ordo.traitements.all().values_list('nom', flat=True)
    doses = ordo.traitements.all().values_list('dose', flat=True)
    consommations = ordo.traitements.all().values_list('consommation', flat=True)

    # Construire le dictionnaire des données à renvoyer
    data = {
        'id': consultation.id,
        'date': consultation.date,
        'resume': consultation.resume,
        'medecin': consultation.medecin.user.last_name if consultation.medecin else None,
        'ordonnance': OrdonnanceSerializer(consultation.ordonnance).data if consultation.ordonnance else None,
        
        'noms': [nom for nom in noms] if noms else [],
        'doses': [dose for dose in doses] if doses else [],
        'consommations': [consommation for consommation in consommations] if consommations else [],

        'bilans_biologiques_prescription': [
            bilan.prescription for bilan in bilansbiologiques
        ] if bilansbiologiques else [],

        'bilans_radiologiques_prescription': [
            bilan.prescription for bilan in bilansradiologiques
        ] if bilansradiologiques else [],

        'bilans_biologiques_resultat': [
            resultat for resultat in resultats
        ] if resultats else [],

        'bilans_radiologiques_compte_rendu': [
            compte_rendu for compte_rendu in compte_rendus
        ] if compte_rendus else [],

        'bilans_radiologiques_url_image': [
           image for image in images
        ] if images else [],
    }

    # Étape 4 : Retourner la réponse au client
    return Response({'data': data}, status=200)



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def get_patient_soins(request):
    """
    Fonction permettant de récupérer tous les soins associés à un patient en fonction de son numéro de sécurité sociale (NSS).

    Cette fonction prend une requête GET contenant le numéro de sécurité sociale (NSS) du patient, 
    puis retourne tous les soins associés au patient correspondant. Si aucun DPI n'est trouvé pour le NSS donné,
    une erreur est renvoyée.

    Arguments :
        request : Requête HTTP contenant le paramètre 'nss' dans les paramètres de la requête GET.

    Retour :
        Response : La liste des soins du patient sous forme de données sérialisées ou un message d'erreur.
    """
    try:
        # Récupérer le NSS depuis les paramètres de la requête
        nss = request.query_params.get('nss')

        # Récupérer le DPI associé au NSS du patient
        dpi = DPI.objects.get(patient__nss=nss)

        # Récupérer tous les soins liés à ce DPI
        soins = Soin.objects.filter(dpi=dpi)

        # Sérialiser les soins récupérés
        serializer = SoinSerializer(soins, many=True)
        print(serializer.data)

        # Retourner les soins sérialisés
        return Response(serializer.data, status=status.HTTP_200_OK)

    except DPI.DoesNotExist:
        # Si aucun DPI n'est trouvé pour le NSS donné
        return Response({'error': 'No DPI found for the given NSS'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        # En cas d'erreur interne du serveur
        return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@api_view(['GET'])
@csrf_exempt  # Assure que l'utilisateur est authentifié (le token est envoyé depuis le front-end pour identifier l'utilisateur)
@authentication_classes([SessionAuthentication, TokenAuthentication])
def get_nss_info(request):
    """
    Fonction permettant de récupérer le numéro de sécurité sociale (NSS) d'un patient en fonction du nom d'utilisateur.

    Cette fonction prend une requête GET avec le nom d'utilisateur ('username') et retourne le numéro de sécurité sociale
    (NSS) associé à ce patient. Le nom d'utilisateur est utilisé pour identifier l'utilisateur authentifié et obtenir
    les informations associées au patient.

    Arguments :
        request : Requête HTTP contenant le paramètre 'username' dans les paramètres de la requête GET.

    Retour :
        Response : Le numéro de sécurité sociale (NSS) du patient ou un message d'erreur si le nom d'utilisateur est absent.
    """
    # Récupérer le nom d'utilisateur depuis les paramètres de la requête GET
    userr = request.GET.get('username') 
    
    # Vérifier si le nom d'utilisateur est fourni
    if not userr:
        return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)  # Le token est envoyé depuis le front-end, à travers lequel on récupère l'utilisateur
    
    print(userr)
    
    # Récupérer l'utilisateur à partir du nom d'utilisateur
    user = CustomUser.objects.get(username=userr)
    
    # Récupérer le patient associé à cet utilisateur
    patient = Patient.objects.get(user=user)
    print(patient)
    
    # Récupérer le numéro de sécurité sociale (NSS) du patient
    nss = patient.nss
    print(nss)
    
    # Retourner le NSS du patient dans la réponse
    return Response({'nss': nss})



@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def get_radiography_image(request):
    """
    Fonction permettant de récupérer une image radiographique à partir de son ID.

    Cette fonction prend une requête GET avec l'ID de l'image radiographique dans les paramètres de la requête. 
    Elle vérifie ensuite si le fichier image correspondant existe sur le serveur. Si l'image est trouvée, elle est 
    renvoyée dans la réponse. Si le fichier n'existe pas ou s'il y a une erreur, une réponse d'erreur est retournée.

    Arguments :
        request : Requête HTTP contenant le paramètre 'id' dans les paramètres de la requête GET, représentant l'ID de l'image.

    Retour :
        Response : Une réponse contenant l'image radiographique si elle est trouvée, ou un message d'erreur si l'image n'existe pas.
    """
    # Récupérer l'ID de l'image depuis les paramètres de la requête GET
    url = request.GET.get('id') 
    
    # Vérifier si l'ID de l'image est fourni
    if not url:
        return Response({"error": "Aucune image"}, status=400)

    # Construire le chemin complet vers le fichier image
    image_path = os.path.join(settings.MEDIA_ROOT, url)

    # Vérifier si le fichier image existe sur le serveur
    if not os.path.exists(image_path):
        return Response({'error': 'Image introuvable.'}, status=404)

    # Tenter de renvoyer l'image dans la réponse
    try:
        print("reponse :", FileResponse(open(image_path, 'rb')))
        # Retourner le fichier image en tant que réponse avec le type de contenu approprié (JPEG)
        return FileResponse(open(image_path, 'rb'), content_type='image/jpeg')
    except Exception as e:
        # Gérer les erreurs imprévues lors de l'ouverture ou de l'envoi de l'image
        return Response({'error': f"Erreur lors de la récupération de l'image: {str(e)}"}, status=500)




@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def get_ordonnance(request, id):
    """
    Fonction permettant de récupérer une ordonnance à partir de son ID.

    Cette fonction prend une requête GET avec l'ID de l'ordonnance dans l'URL et retourne les informations de l'ordonnance
    sous forme de données sérialisées. Si l'ordonnance n'est pas trouvée, une erreur est renvoyée.

    Arguments :
        request : Requête HTTP contenant l'ID de l'ordonnance dans l'URL.
        id : L'ID de l'ordonnance à récupérer.

    Retour :
        Response : Les données sérialisées de l'ordonnance si elle est trouvée, ou un message d'erreur si l'ordonnance n'existe pas.
    """
    try:
        # Récupérer l'ordonnance en fonction de son ID
        ordonnance = Ordonnance.objects.get(id=id)
        
        # Sérialiser les données de l'ordonnance
        serializer = OrdonnanceSerializer(ordonnance)
        
        # Retourner les données sérialisées de l'ordonnance
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Ordonnance.DoesNotExist:
        # Si l'ordonnance n'existe pas dans la base de données
        return Response({'error': 'Ordonnance introuvable'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def valider_ordonnance(request, id):
    """
    Fonction permettant de valider une ordonnance en fonction de son ID.

    Cette fonction prend une requête POST contenant un paramètre de validation dans le corps de la requête et valide ou
    invalide l'ordonnance associée à l'ID fourni. Si l'ordonnance est déjà validée, un message d'erreur est retourné. 
    Si l'ordonnance est validée ou invalidée avec succès, un message de confirmation est renvoyé.

    Arguments :
        request : Requête HTTP contenant le paramètre 'validation' dans le corps de la requête, indiquant la validation de l'ordonnance.
        id : L'ID de l'ordonnance à valider.

    Retour :
        Response : Un message confirmant la validation de l'ordonnance ou un message d'erreur si l'ordonnance est déjà validée ou introuvable.
    """
    # Récupérer l'ordonnance par son ID
    ordonnance = Ordonnance.objects.get(id=id)
    
    # Vérifier si l'ordonnance existe
    if not ordonnance:
        return Response({'error': 'Ordonnance introuvable'}, status=404)
    
    # Vérifier si l'ordonnance est déjà validée
    if ordonnance.validee:
        return Response({'message': 'Ordonnance déjà validée'}, status=400)

    # Récupérer la réponse de validation (True ou False)
    sgph_response = request.data.get('validation') 
    
    # Mettre à jour le statut de validation de l'ordonnance
    ordonnance.validee = sgph_response
    ordonnance.save()

    # Préparer le message de réponse selon que l'ordonnance soit validée ou non
    status_message = 'validée' if sgph_response else 'non validée'
    
    # Retourner un message de confirmation
    return Response({'message': f"Ordonnance {status_message}"}, status=200)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def distribuer_medicament(request):
    """
    Fonction permettant au SGPH de distribuer un médicament en fonction d'une ordonnance et d'un traitement.

    Cette fonction prend une requête POST avec l'ID de l'ordonnance, l'ID du traitement et la quantité à distribuer. 
    Elle vérifie si l'ordonnance est valide et si le traitement existe avant de créer une distribution. La distribution 
    est ensuite retournée dans la réponse sous forme sérialisée.

    Arguments :
        request : Requête HTTP contenant les paramètres 'ordonnance_id', 'traitement_id' et 'quantite' dans le corps de la requête.

    Retour :
        Response : Les données sérialisées de la distribution créée, ou un message d'erreur si l'ordonnance est invalide, le traitement introuvable, ou d'autres erreurs.
    """
    # Récupérer l'ID de l'ordonnance, du traitement et la quantité depuis la requête
    ordonnance_id = request.data.get('ordonnance_id')
    traitement_id = request.data.get('traitement_id')
    quantite = request.data.get('quantite')

    # Vérifier si l'ordonnance existe et si elle est validée
    ordonnance = Ordonnance.objects.filter(id=ordonnance_id).first()
    if not ordonnance or not ordonnance.validee:
        return Response({'error': 'Ordonnance invalide ou non validée'}, status=400)

    # Vérifier si le traitement existe
    traitement = Traitement.objects.filter(id=traitement_id).first()
    if not traitement:
        return Response({'error': 'Traitement introuvable'}, status=404)

    # Créer une nouvelle distribution de médicament
    distribution = Distribution.objects.create(
        ordonnance=ordonnance,
        traitement=traitement,
        quantite=quantite
    )

    # Sérialiser les données de la distribution
    serializer = DistributionSerializer(distribution)

    # Retourner la distribution créée dans la réponse
    return Response(serializer.data, status=201)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def export_bilans_bio(request):
    """
    Fonction permettant d'exporter tous les bilans biologiques.

    Cette fonction prend une requête GET et retourne tous les bilans biologiques sous forme sérialisée. 
    Si aucun bilan biologique n'est trouvé, une erreur est renvoyée.

    Arguments :
        request : Requête HTTP sans paramètres spécifiques (juste la requête GET).

    Retour :
        Response : Les données sérialisées de tous les bilans biologiques trouvés, ou un message d'erreur si aucun bilan biologique n'est disponible.
    """
    # Récupérer tous les bilans biologiques
    biologiques = BilanBiologique.objects.all()

    # Vérifier si des bilans biologiques existent
    if not biologiques:
        return Response({'error': 'Aucun bilan biologique trouvé'}, status=status.HTTP_404_NOT_FOUND)

    # Sérialiser les données des bilans biologiques
    serializer = BiologiqueSerializer(biologiques, many=True)

    # Afficher les données sérialisées (pour débogage)
    print(serializer.data)

    # Retourner les bilans biologiques sous forme sérialisée
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def export_bilans_radio(request):
    """
    Fonction permettant d'exporter tous les bilans radiologiques.

    Cette fonction prend une requête GET et retourne tous les bilans radiologiques sous forme sérialisée. 
    Si aucun bilan radiologique n'est trouvé, une erreur est renvoyée.

    Arguments :
        request : Requête HTTP sans paramètres spécifiques (juste la requête GET).

    Retour :
        Response : Les données sérialisées de tous les bilans radiologiques trouvés, ou un message d'erreur si aucun bilan radiologique n'est disponible.
    """
    # Récupérer tous les bilans radiologiques
    radiologiques = BilanRadiologique.objects.all()

    # Vérifier si des bilans radiologiques existent
    if not radiologiques:
        return Response({'error': 'Aucun bilan radiologique trouvé'}, status=status.HTTP_404_NOT_FOUND)

    # Sérialiser les données des bilans radiologiques
    serializer = RadiologiqueSerializer(radiologiques, many=True)

    # Afficher les données sérialisées (pour débogage)
    print(serializer.data)

    # Retourner les bilans radiologiques sous forme sérialisée
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def export_radio(request):
    """
    Fonction permettant d'exporter les bilans radiologiques sans compte rendu.

    Cette fonction prend une requête GET et retourne tous les bilans radiologiques où le compte rendu est vide. 
    Si aucun bilan radiologique correspondant n'est trouvé, une erreur est renvoyée.

    Arguments :
        request : Requête HTTP sans paramètres spécifiques (juste la requête GET).

    Retour :
        Response : Les données sérialisées de tous les bilans radiologiques sans compte rendu trouvés, ou un message d'erreur si aucun bilan radiologique n'est disponible.
    """
    # Récupérer tous les bilans radiologiques où le compte rendu est vide
    radiologiques = BilanRadiologique.objects.filter(compte_rendu='')

    # Vérifier si des bilans radiologiques sont trouvés
    if not radiologiques:
        return Response({'error': 'Aucun bilan radiologique trouvé'}, status=status.HTTP_404_NOT_FOUND)

    # Sérialiser les données des bilans radiologiques
    serializer = RadiologiqueSerializer(radiologiques, many=True)

    # Retourner les bilans radiologiques sérialisés
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def envoi_pres_bio(request):
    """
    Fonction permettant d'envoyer la prescription associée à un bilan biologique.

    Cette fonction prend une requête GET avec un paramètre 'id' pour récupérer un bilan biologique. 
    Si le bilan existe, sa prescription est renvoyée dans la réponse. En cas d'absence de l'identifiant ou si le bilan 
    biologique n'est pas trouvé, une erreur est renvoyée.

    Arguments :
        request : Requête HTTP avec un paramètre GET 'id' qui correspond à l'ID du bilan biologique.

    Retour :
        Response : La prescription du bilan biologique sous forme de réponse, ou un message d'erreur si l'ID est manquant ou si le bilan n'est pas trouvé.
    """
    # Récupérer l'ID du bilan biologique depuis la requête
    id = request.GET.get('id') 

    # Vérifier si l'ID est fourni
    if not id:
        return Response({"error": "L'identifiant (id) est requis."}, status=400)

    try:
        # Récupérer le bilan biologique correspondant à l'ID
        bilan = BilanBiologique.objects.get(id=id)
    except BilanBiologique.DoesNotExist:
        # Retourner une erreur si le bilan biologique n'existe pas
        return Response({'error': 'Bilan introuvable.'}, status=404)

    # Retourner la prescription du bilan biologique
    return Response(bilan.prescription, status=200)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def envoi_pres_radio(request):
    """
    Fonction permettant d'envoyer la prescription associée à un bilan radiologique.

    Cette fonction prend une requête GET avec un paramètre 'id' pour récupérer un bilan radiologique. 
    Si le bilan existe, sa prescription est renvoyée dans la réponse. En cas d'absence de l'identifiant ou si le bilan 
    radiologique n'est pas trouvé, une erreur est renvoyée.

    Arguments :
        request : Requête HTTP avec un paramètre GET 'id' qui correspond à l'ID du bilan radiologique.

    Retour :
        Response : La prescription du bilan radiologique sous forme de réponse, ou un message d'erreur si l'ID est manquant ou si le bilan n'est pas trouvé.
    """
    # Récupérer l'ID du bilan radiologique depuis la requête
    id = request.GET.get('id') 

    # Vérifier si l'ID est fourni
    if not id:
        return Response({"error": "L'identifiant (id) est requis."}, status=400)

    try:
        # Récupérer le bilan radiologique correspondant à l'ID
        bilan = BilanRadiologique.objects.get(id=id)
    except BilanRadiologique.DoesNotExist:
        # Retourner une erreur si le bilan radiologique n'existe pas
        return Response({'error': 'Bilan introuvable.'}, status=404)

    # Retourner la prescription du bilan radiologique
    return Response(bilan.prescription, status=200)


@csrf_exempt
@authentication_classes([SessionAuthentication, TokenAuthentication])
def remplir_bilan_bio(request):
    """
    Fonction permettant de remplir un bilan biologique avec des mesures.

    Cette fonction prend une requête POST contenant les mesures pour un bilan biologique spécifique. 
    Si le bilan existe, les mesures sont ajoutées à celui-ci. Si le bilan biologique ou les données sont incorrectes,
    des erreurs sont renvoyées.

    Arguments :
        request : Requête HTTP contenant le corps de la requête avec les mesures à ajouter au bilan biologique.

    Retour :
        JsonResponse : Retourne un message de succès avec l'ID du bilan biologique en cas de réussite, ou un message d'erreur en cas de problème (format JSON invalide, bilan introuvable, etc.).
    """
    if request.method == 'POST':
        try:
            # Charger et analyser le corps de la requête
            body = json.loads(request.body)
            idb = request.GET.get('id')  # Récupérer l'ID du bilan biologique depuis les paramètres GET
            measures = json.loads(body.get('measures'))  # Extraire les mesures depuis le corps de la requête
            
            # Vérifier si l'ID du bilan biologique est fourni
            if not idb:
                return JsonResponse({"error": "L'identifiant du bilan (idb) est requis."}, status=400)

            try:
                # Récupérer le bilan biologique avec l'ID spécifié
                bilan = BilanBiologique.objects.get(id=idb)
            except BilanBiologique.DoesNotExist:
                # Retourner une erreur si le bilan biologique n'est pas trouvé
                return JsonResponse({"error": "Bilan radiologique introuvable."}, status=404)
            
            # Construire le résultat à partir des mesures fournies
            resultat = "\n".join(
               f"{item.get('mesure', '')} : {item.get('valeur', '')}" for item in measures
            )

            # Sauvegarder les résultats dans le bilan biologique
            bilan.resultat = resultat
            bilan.save()

            # Retourner un message de succès
            return JsonResponse({"message": "Bilan ajouté avec succès.", "bilan_id": bilan.id}, status=201)

        except json.JSONDecodeError:
            # Gérer l'erreur si le corps de la requête n'est pas un JSON valide
            return JsonResponse({"error": "Le corps de la requête doit être au format JSON valide."}, status=400)
        except Exception as e:
            # Gérer les erreurs inattendues
            return JsonResponse({"error": f"Erreur inattendue : {str(e)}"}, status=500)

    # Retourner une erreur pour les méthodes non autorisées
    return JsonResponse({"error": "Méthode non autorisée. Utilisez POST."}, status=405)

@csrf_exempt
@authentication_classes([SessionAuthentication, TokenAuthentication])
def remplir_bilan_radio(request):
    """
    Fonction permettant de remplir un bilan radiologique avec une image et un compte-rendu.

    Cette fonction prend une requête POST contenant une image et un compte-rendu pour un bilan radiologique spécifique.
    Si le bilan existe, l'image et le compte-rendu sont ajoutés à celui-ci. Si le bilan radiologique ou les données sont incorrectes,
    des erreurs sont renvoyées.

    Arguments :
        request : Requête HTTP contenant le fichier d'image et le compte-rendu à ajouter au bilan radiologique.

    Retour :
        JsonResponse : Retourne un message de succès avec l'ID du bilan radiologique en cas de réussite, ou un message d'erreur en cas de problème (bilan introuvable, fichier manquant, etc.).
    """
    if request.method == 'POST':
        try:
            idb = request.GET.get('id')  # Récupérer l'ID du bilan radiologique depuis les paramètres GET
            if not idb:
                # Si l'ID du bilan radiologique n'est pas fourni, renvoyer une erreur
                return JsonResponse({"error": "L'identifiant du bilan (idb) est requis."}, status=400)

            try:
                # Récupérer le bilan radiologique avec l'ID spécifié
                bilan = BilanRadiologique.objects.get(id=idb)
            except BilanRadiologique.DoesNotExist:
                # Retourner une erreur si le bilan radiologique n'est pas trouvé
                return JsonResponse({"error": "Bilan radiologique introuvable."}, status=404)

            # Traiter l'upload du fichier image et le compte-rendu
            image = request.FILES.get('image')  # Récupérer l'image envoyée dans la requête
            compte_rendu = request.POST.get('compteRendu')  # Récupérer le compte-rendu depuis les données du formulaire
            
            # Si une image est fournie, l'assigner au modèle
            if image:
                bilan.image = image
            # Si un compte-rendu est fourni, l'assigner au modèle
            if compte_rendu:
                bilan.compte_rendu = compte_rendu

            # Sauvegarder les modifications dans le modèle
            bilan.save()

            # Retourner un message de succès
            return JsonResponse({"message": "Bilan ajouté avec succès.", "bilan_id": bilan.id}, status=201)

        except Exception as e:
            # Gérer toute erreur inattendue et renvoyer un message d'erreur
            return JsonResponse({"error": f"Erreur inattendue : {str(e)}"}, status=500)

    # Retourner une erreur si la méthode n'est pas POST
    return JsonResponse({"error": "Méthode non autorisée. Utilisez POST."}, status=405)












###################################################################################################################


import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

def bilan_type_detector(consigne, model=None, vectorizer=None):
    """
    Retourne True si le bilan est biologique, False s'il est radiologique.
    
    Args:
        consigne (str): La consigne décrivant le bilan.
        model (trained model): Modèle entraîné (si déjà chargé)
        vectorizer (trained vectorizer): Vectorizer entraîné (si déjà chargé)
    
    Returns:
        bool: True pour biologique, False pour radiologique.
    """
    # Si le modèle et le vectorizer ne sont pas fournis, on les charge depuis un fichier pickle
    if model is None or vectorizer is None:
        with open('model_bilan.pkl', 'rb') as model_file:
            model, vectorizer = pickle.load(model_file)
    
    # Prédire le type de bilan à partir de la consigne
    X_test = vectorizer.transform([consigne])
    prediction = model.predict(X_test)
    
    # Retourner le résultat
    return bool(prediction[0])

def entrainer_et_sauvegarder_model():
    """
    Entraîne le modèle et le sauvegarde dans un fichier pickle.
    """
    # Données d'entraînement étendues
    consignes = [
        # Biologiques (35)
        "Analyse de sang pour le cholestérol", "Test de glycémie à jeun", "Dosage des hormones thyroïdiennes",
        "Bilan urinaire pour une infection", "Hémogramme pour vérifier les globules rouges", 
        "Recherche de marqueurs tumoraux dans le sang", "Dosage du calcium sanguin", "Analyse de liquide céphalorachidien", 
        "Test d'hémoglobine glyquée", "Culture d'urine pour identifier une bactérie", "Dosage des électrolytes dans le plasma", 
        "Analyse du liquide pleural", "Test de dépistage du VIH", "Test d'antigène pour la grippe", "Recherche d'anticorps dans le sang",
        "Dosage des enzymes hépatiques", "Analyse de sang pour le fer sérique", "Test de dépistage de la syphilis", 
        "Analyse d'urine pour détecter des protéines", "Recherche de pathogènes dans les selles", "Test sanguin pour mesurer le taux d'albumine",
        "Test de dépistage du paludisme", "Analyse du liquide synovial", "Bilan rénal pour évaluer la fonction des reins",
        "Dosage de la troponine cardiaque", "Analyse de la ferritine dans le sang", "Culture de plaie pour identifier une infection",
        "Dosage de la vitamine D", "Analyse de sang pour le taux de CRP", "Recherche de parasites dans le sang", 
        "Test sanguin pour mesurer le taux d'acide urique", "Analyse de sang pour le groupe sanguin", 
        "Test de dépistage des hépatites virales", "Analyse de gaz du sang artériel", "Test de coagulation pour le temps de prothrombine",
        
        # Radiologiques (35)
        "IRM cérébrale pour détecter une tumeur", "Scanner thoracique pour une embolie pulmonaire", "Radiographie des poumons pour une pneumonie",
        "Échographie abdominale pour une douleur", "IRM lombaire pour une hernie discale", "Radiographie dentaire pour une carie", 
        "Tomodensitométrie du genou pour une fracture", "Radiographie de la colonne pour une scoliose", "Mammographie pour dépister un cancer du sein", 
        "Échographie cardiaque pour une anomalie", "IRM du genou pour une lésion ligamentaire", "Scanner abdominopelvien pour une appendicite", 
        "Arthro-IRM pour une lésion articulaire", "Radiographie de la main pour une fracture", "Échographie pelvienne pour une masse ovarienne",
        "Radiographie du bassin pour une fracture", "IRM du poignet pour une douleur chronique", "Scanner cérébral pour un AVC", 
        "Radiographie de l'épaule pour une luxation", "Échographie hépatique pour détecter une stéatose", "Radiographie thoracique pour une douleur",
        "IRM thoracique pour des anomalies cardiaques", "Scanner des sinus pour une sinusite", "Radiographie des dents pour un implant", 
        "Échographie transvaginale pour une grossesse", "IRM de la hanche pour une nécrose", "Scanner abdominal pour un kyste rénal", 
        "Radiographie des vertèbres cervicales pour un traumatisme", "Mammographie de dépistage annuel", "Échographie rénale pour des calculs",
        "Radiographie pulmonaire pour un cancer suspecté", "IRM orbitale pour une tumeur de l'œil", "Scanner du cœur pour évaluer les coronaires", 
        "IRM du pied pour détecter une fracture", "Échographie doppler des artères carotides"
    ]
    
    # Labels associés : 1 = biologique, 0 = radiologique
    labels = [1] * 35 + [0] * 35  # 1 pour biologique, 0 pour radiologique
    
    # Vectorisation des données
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(consignes)
    
    # Entraîner le modèle Naive Bayes
    model = MultinomialNB()
    model.fit(X, labels)
    
    # Sauvegarder le modèle et le vectorizer
    with open('model_bilan.pkl', 'wb') as model_file:
        pickle.dump((model, vectorizer), model_file)

# Entraîner le modèle et sauvegarder
entrainer_et_sauvegarder_model()






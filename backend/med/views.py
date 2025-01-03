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
    Traitement   )
from .serializers import PatientSerializer, PatientMinimalSerializer, SoinSerializer
from users.decorators import role_required
from users.serializers import UserSerializer
from .utils import generate_qrcode
from django.utils.timezone import now
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

@api_view(['POST'])
def rediger_soin(request):
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
                dpi = dpi,
                date_emission = now()
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
                            date_emission = now(),
                            prescription=consigne,
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

from users.models import CustomUser


@api_view(['GET'])
def MedecinView(request):
    print('hna')
    username = request.GET.get('username') 
    print(username)
    if not username:
        return Response({"error": "Username is required."}, status=400)
        
    try:
        user = CustomUser.objects.get(username=username)
        medecin = Medecin.objects.get(user=user)
    except CustomUser.DoesNotExist:
        raise NotFound("User with this username does not exist.")
    except Medecin.DoesNotExist:
        raise NotFound("No Medecin profile found for this user.")
        
    return Response({
        "first_name": user.first_name,
        "last_name": user.last_name,
        "specialite": medecin.specialite
    })



















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

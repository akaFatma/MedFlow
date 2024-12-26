import json
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import ( 
    Patient, 
    PersonneAContacter, 
    DPI,
    Traitement
)

# Page d'accueil
def home(request):
    return HttpResponse("Bienvenue sur la page d'accueil!")

# Définir un décorateur de gestion des rôles
def check_roles(allowed_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Utilisateur non authentifié'}, status=403)
            if request.user.role not in allowed_roles:
                return JsonResponse({'error': f'Accès refusé pour ce rôle: {request.user.role}'}, status=403)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# Création du DPI - Gestion de la création des patients et de la personne à contacter
@csrf_exempt
# @check_roles(['admin', 'medecin'])

def creer_dpi(request): 
    if request.method == 'POST':
        try:
            # Décodage des données envoyées en JSON dans le corps de la requête
            body = json.loads(request.body)
            print(f"Données reçues : {body}")  # Affiche les données JSON dans la console pour débogage

            step = body.get('step')
            data = body.get('data')

            if not data and (step == 2 or step == 1):
                return JsonResponse({'error': 'Aucune donnée fournie'}, status=400)

            # Variables par défaut pour les étapes 2 et 3
            nom_personne = prenom_personne = telephone_personne = None
            nom = prenom = date_naissance = telephone = adr = nss = mutuelle = None

            if step == 1:
                # Étape 1 : Collecte des données personnelles
                nom = data.get('nom')
                prenom = data.get('prenom')
                date_naissance = data.get('date')
                telephone = data.get('telephone')

                # Enregistrer les données de l'étape 1 dans la session
                request.session['nom'] = nom
                request.session['prenom'] = prenom
                request.session['date_naissance'] = date_naissance
                request.session['telephone'] = telephone
                print(request.session.items())

                if not all([nom, prenom, date_naissance, telephone]):
                    return JsonResponse({'error': 'Certains champs sont manquants dans l\'étape 1'}, status=400)

                return JsonResponse({'message': 'Étape 1 complétée', 'data': {
                    'nom': nom,
                    'prenom': prenom,
                    'date_naissance': date_naissance,
                    'telephone': telephone,
                }})

            elif step == 2:
                # Étape 2 : Collecte des données supplémentaires
                nss = data.get('nss')
                mutuelle = data.get('mutuelle')
                nom_personne = data.get('personne_nom')
                prenom_personne = data.get('personne_prenom')
                telephone_personne = data.get('personne_telephone')
                adr = data.get('adresse')

                # Enregistrer les données de l'étape 2 dans la session
                request.session['nss'] = nss
                request.session['mutuelle'] = mutuelle
                request.session['nom_personne'] = nom_personne
                request.session['prenom_personne'] = prenom_personne
                request.session['telephone_personne'] = telephone_personne
                request.session['adresse'] = adr
                print(request.session.items())

                if not all([nss, mutuelle, nom_personne, prenom_personne, telephone_personne]):
                    return JsonResponse({'error': 'Certains champs sont manquants dans l\'étape 2'}, status=400)

                return JsonResponse({'message': 'Étape 2 complétée', 'data': {
                    'nss': nss,
                    'mutuelle': mutuelle,
                    'nom_personne': nom_personne,
                    'prenom_personne': prenom_personne,
                    'telephone_personne': telephone_personne
                }})

            elif step == 3:
                # Étape 3 : Création des objets et validation
                print(f"Session data: {dict(request.session)}")
                nom = request.session.get('nom')
                prenom = request.session.get('prenom')
                date_naissance = request.session.get('date_naissance')
                telephone = request.session.get('telephone')
                adr = request.session.get('adresse')
                nss = request.session.get('nss')
                mutuelle = request.session.get('mutuelle')
                nom_personne = request.session.get('nom_personne')
                prenom_personne = request.session.get('prenom_personne')
                telephone_personne = request.session.get('telephone_personne')

                if nom_personne and prenom_personne and telephone_personne:
                    personne_a_contacter, created = PersonneAContacter.objects.get_or_create(
                        nom=nom_personne,
                        prenom=prenom_personne,
                        telephone=telephone_personne
                    )

                    patient = Patient.objects.create(
                        nom=nom, prenom=prenom, date_de_naissance=date_naissance,
                        adresse=adr, telephone=telephone, nss=nss, mutuelle=mutuelle,
                        personne_a_contacter=personne_a_contacter
                    )

                    dpi = DPI.objects.create(patient=patient)

                    return JsonResponse({'message': 'DPI créé avec succès', 'data': {
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
                    }})

                return JsonResponse({'error': 'Données incomplètes pour l\'étape 3'}, status=400)

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


###########################################Nouvelle version de creer_dpi#############################################

@csrf_exempt
def creerr_dpi(request): 
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
            date_naissance = data.get('date')
            telephone = data.get('telephone')
            adr = data.get('adresse')
            nss = data.get('nss')
            mutuelle = data.get('mutuelle')
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

# Rédaction d'ordonnance - Traitements
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
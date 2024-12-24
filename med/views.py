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
            body = json.loads(request.body)
            step = body.get('step')
            data = body.get('data')

            # Vérification des données
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
                adr = data.get('adresse')

                if not all([nom, prenom, date_naissance, telephone, adr]):
                    return JsonResponse({'error': 'Certains champs sont manquants dans l\'étape 1'}, status=400)

                # Réponse pour l'étape 1
                return JsonResponse({'message': 'Données de l’étape 1 traitées avec succès'})

            elif step == 2:
                # Étape 2 : Collecte des données de sécurité sociale et contact d'urgence
                nss = data.get('nss')
                mutuelle = data.get('mutuelle')
                nom_personne = data.get('personne_nom')
                prenom_personne = data.get('personne_prenom')
                telephone_personne = data.get('personne_telephone')

                if not all([nss, mutuelle, nom_personne, prenom_personne, telephone_personne]):
                    return JsonResponse({'error': 'Certains champs sont manquants dans l\'étape 2'}, status=400)

                # Réponse pour l'étape 2
                return JsonResponse({'message': 'Données de l’étape 2 traitées avec succès'})

            elif step == 3:
                # Étape 3 : Création de la personne à contacter et du patient
                if nom_personne and prenom_personne and telephone_personne:
                    personne_a_contacter = PersonneAContacter.objects.create(
                        nom=nom_personne, prenom=prenom_personne, telephone=telephone_personne)

                    # Collecte des informations de la personne à contacter pour la réponse JSON
                    personne_data = {
                        'id': personne_a_contacter.id,
                        'nom': personne_a_contacter.nom,
                        'prenom': personne_a_contacter.prenom,
                        'telephone': personne_a_contacter.telephone
                    }

                    # Création du patient
                    patient = Patient.objects.create(
                        nom=nom, prenom=prenom, date_naissance=date_naissance, adresse=adr, 
                        telephone=telephone, nss=nss, mutuelle=mutuelle, personne_a_contacter=personne_a_contacter)

                    # Création du DPI
                    dpi = DPI.objects.create(patient=patient)

                    # Réponse JSON avec les données de la personne à contacter et du DPI
                    return JsonResponse({'personne_a_contacter': personne_data, 'dpi': str(dpi)})

                # Si les données ne sont pas valides, retourner un message générique
                return JsonResponse({'message': 'Données de l’étape 3 traitées avec succès'})

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

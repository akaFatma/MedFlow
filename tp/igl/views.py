"""
import logging
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import Patient, DPI, Consultation, CertificatMedical

# Initialiser le logger
logger = logging.getLogger(__name__)

@csrf_exempt
def demander_certificat_medical(request, patient_nss):
    logger.info(f"Requête reçue pour le patient avec NSS: {patient_nss}")
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            description = body.get('description', '')
            date_consultation = body.get('date_consultation', '')

            if not date_consultation:
                logger.error("La date de la consultation est obligatoire.")
                return JsonResponse({"error": "La date de la consultation est obligatoire."}, status=400)

            try:
                date_consultation = datetime.strptime(date_consultation, "%Y-%m-%d").date()
            except ValueError:
                logger.error("Format de date invalide. Utilisez 'YYYY-MM-DD'.")
                return JsonResponse({"error": "Format de date invalide. Utilisez 'YYYY-MM-DD'."}, status=400)

            logger.info(f"Recherche du patient avec NSS: {patient_nss}")
            
            try:
                patient = Patient.objects.get(nss=patient_nss)
                logger.info(f"Patient trouvé: {patient.nom} {patient.prenom}")
            except Patient.DoesNotExist:
                logger.error(f"Patient non trouvé pour NSS: {patient_nss}")
                return JsonResponse({"error": "Patient non trouvé."}, status=404)

            consultation = Consultation.objects.filter(dpi__patient=patient, date=date_consultation).first()

            if not consultation:
                logger.error("Aucune consultation trouvée pour cette date.")
                return JsonResponse({"error": "Aucune consultation trouvée pour cette date."}, status=404)

            logger.info(f"Consultation trouvée pour la date: {date_consultation}")

            certificat = CertificatMedical(
                consultation=consultation,
                patient=patient,
                date=date_consultation,
                justification_medecin=description
            )
            certificat.save()

            medecin = consultation.ordonnance.medecins.first() if consultation.ordonnance else None
            logger.info(f"Médecin associé : {medecin.nom} {medecin.prenom}" if medecin else "Aucun médecin associé")

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="certificat_medical_{patient_nss}.pdf"'

            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)

            p.drawString(100, 750, f"Certificat Médical - Patient {patient.nom} {patient.prenom}")
            p.drawString(100, 730, f"NSS: {patient.nss}")
            p.drawString(100, 710, f"Date de Consultation: {date_consultation}")
            p.drawString(100, 690, f"Description: {description}")
            p.drawString(100, 670, f"Médecin: {medecin.nom} {medecin.prenom}" if medecin else "Médecin: Aucun médecin associé")
            p.drawString(100, 650, f"Date de création du certificat: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            p.showPage()
            p.save()

            buffer.seek(0)
            response.write(buffer.getvalue())
            return response

        except json.JSONDecodeError:
            logger.error("Données JSON invalides.")
            return JsonResponse({"error": "Données JSON invalides."}, status=400)
        except ValueError:
            logger.error("Valeurs invalides.")
            return JsonResponse({"error": "Valeurs invalides."}, status=400)
        except Exception as e:
            logger.error(f"Erreur inattendue : {str(e)}")
            return JsonResponse({"error": "Erreur inattendue."}, status=500)
    return JsonResponse({"error": "Méthode non autorisée."}, status=405)
"""

"""
@csrf_exempt
def ajouter_patient(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            nom = body.get('nom', '')
            prenom = body.get('prenom', '')
            date_de_naissance = body.get('date_de_naissance', '')
            adresse = body.get('adresse', '')
            telephone = body.get('telephone', '')
            nss = body.get('nss', '')
            mutuelle = body.get('mutuelle', '')
            personne_a_contacter_nom = body.get('personne_a_contacter_nom', '')
            personne_a_contacter_prenom = body.get('personne_a_contacter_prenom', '')
            personne_a_contacter_telephone = body.get('personne_a_contacter_telephone', '')
            utilisateur_id = body.get('utilisateur_id', '')

            if not date_de_naissance:
                return JsonResponse({"error": "La date de naissance est obligatoire."}, status=400)

            try:
                date_de_naissance = datetime.strptime(date_de_naissance, "%Y-%m-%d").date()
            except ValueError:
                return JsonResponse({"error": "Format de date invalide. Utilisez 'YYYY-MM-DD'."}, status=400)

            personne_a_contacter = PersonneAContacter.objects.create(
                nom=personne_a_contacter_nom,
                prenom=personne_a_contacter_prenom,
                telephone=personne_a_contacter_telephone
            )

            patient = Patient.objects.create(
                nom=nom,
                prenom=prenom,
                date_de_naissance=date_de_naissance,
                adresse=adresse,
                telephone=telephone,
                nss=nss,
                mutuelle=mutuelle,
                personne_a_contacter=personne_a_contacter
            )

            try:
                utilisateur = Utilisateur.objects.get(id=utilisateur_id)
            except Utilisateur.DoesNotExist:
                return JsonResponse({"error": "Utilisateur non trouvé."}, status=404)

            dpi = DPI.objects.create(
                patient=patient,
                utilisateur=utilisateur
            )

            return JsonResponse({"message": "Patient et DPI ajoutés avec succès.", "patient_id": patient.id, "dpi_id": dpi.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Données JSON invalides."}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Erreur inattendue : {str(e)}"}, status=500)
    return JsonResponse({"error": "Méthode non autorisée."}, status=405)

"""
"""
def consulter_dpi(request, dpi_id):
    try:
        dpi = DPI.objects.get(id=dpi_id)
        patient = dpi.patient

        data = {
            'patient': {
                'id': patient.id,
                'nom': patient.nom,
                'prenom': patient.prenom,
                'date_de_naissance': patient.date_de_naissance.strftime('%Y-%m-%d'),
                'adresse': patient.adresse,
                'telephone': patient.telephone,
                'nss': patient.nss,
                'mutuelle': patient.mutuelle,
                'personne_a_contacter': {
                    'nom': patient.personne_a_contacter.nom,
                    'prenom': patient.personne_a_contacter.prenom,
                    'telephone': patient.personne_a_contacter.telephone
                }
            },
            'utilisateur': {
                'id': dpi.utilisateur.id,
                'username': dpi.utilisateur.username,
                'telephone': dpi.utilisateur.telephone,
                'etablissement_id': dpi.utilisateur.etablissement_id
            }
        }
        return JsonResponse(data, status=200)

    except DPI.DoesNotExist:
        return JsonResponse({"error": "DPI non trouvé."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"Erreur inattendue : {str(e)}"}, status=500)
"""







"""
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import BilanBiologique, BilanRadiologique, Consultation, Patient, PersonneAContacter, Utilisateur, DPI
import json
from datetime import datetime
@csrf_exempt
def remplir_bilan(request, consultation_id, type_bilan):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            prescription = body.get('prescription', '')
            resultat = body.get('resultat', '')
            compte_rendu = body.get('compte_rendu', '')
            image_url = body.get('image_url', '')

            try:
                consultation = Consultation.objects.get(id=consultation_id)
            except Consultation.DoesNotExist:
                return JsonResponse({"error": "Consultation non trouvée."}, status=404)

            if type_bilan == 'biologique':
                bilan = BilanBiologique.objects.create(
                    consultation=consultation,
                    prescription=prescription,
                    resultat=resultat
                )
            elif type_bilan == 'radiologique':
                bilan = BilanRadiologique.objects.create(
                    consultation=consultation,
                    prescription=prescription,
                    compte_rendu=compte_rendu,
                    image_url=image_url
                )
            else:
                return JsonResponse({"error": "Type de bilan invalide."}, status=400)

            return JsonResponse({"message": "Bilan ajouté avec succès.", "bilan_id": bilan.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Données JSON invalides."}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Erreur inattendue : {str(e)}"}, status=500)
    return JsonResponse({"error": "Méthode non autorisée."}, status=405)



import matplotlib.pyplot as plt
import io
import base64
from django.http import JsonResponse

def generer_graphique_bilan_biologique(request, consultation_id):
    try:
        bilans = BilanBiologique.objects.filter(consultation_id=consultation_id).order_by('date_emission')
        
        dates = [bilan.date_emission for bilan in bilans]
        resultats = [float(bilan.resultat) for bilan in bilans]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, resultats, marker='o', linestyle='-', color='b')
        plt.title('Tendance des résultats biologiques')
        plt.xlabel('Date')
        plt.ylabel('Résultats')
        plt.grid(True)

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        image_png = buffer.getvalue()
        buffer.close()

        image_base64 = base64.b64encode(image_png)
        image_base64_str = image_base64.decode('utf-8')

        return JsonResponse({'graphique': image_base64_str})

    except Exception as e:
        return JsonResponse({"error": f"Erreur inattendue : {str(e)}"}, status=500)



from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Consultation, Patient, DPI
import json
from datetime import datetime

@csrf_exempt
def ajouter_consultation(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            patient_id = body.get('patient_id', '')
            date = body.get('date', '')
            resume = body.get('resume', '')
            dpi_id = body.get('dpi_id', '')

            try:
                patient = Patient.objects.get(id=patient_id)
            except Patient.DoesNotExist:
                return JsonResponse({"error": "Patient non trouvé."}, status=404)

            try:
                dpi = DPI.objects.get(id=dpi_id)
            except DPI.DoesNotExist:
                return JsonResponse({"error": "DPI non trouvé."}, status=404)

            try:
                date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                return JsonResponse({"error": "Format de date invalide. Utilisez 'YYYY-MM-DD'."}, status=400)

            consultation = Consultation.objects.create(
                dpi=dpi,
                date=date,
                resume=resume
            )

            return JsonResponse({"message": "Consultation ajoutée avec succès.", "consultation_id": consultation.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Données JSON invalides."}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Erreur inattendue : {str(e)}"}, status=500)
    return JsonResponse({"error": "Méthode non autorisée."}, status=405)

"""


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import BilanBiologique, BilanRadiologique, Consultation
import json
from datetime import datetime

@csrf_exempt
def remplir_bilan(request, consultation_id, type_bilan):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            prescription = body.get('prescription', '')
            resultat = body.get('resultat', '')
            compte_rendu = body.get('compte_rendu', '')
            image_url = body.get('image_url', '')

            try:
                consultation = Consultation.objects.get(id=consultation_id)
            except Consultation.DoesNotExist:
                return JsonResponse({"error": "Consultation non trouvée."}, status=404)

            if type_bilan == 'biologique':
                bilan = BilanBiologique.objects.create(
                    consultation=consultation,
                    prescription=prescription,
                    resultat=resultat
                )
            elif type_bilan == 'radiologique':
                bilan = BilanRadiologique.objects.create(
                    consultation=consultation,
                    prescription=prescription,
                    compte_rendu=compte_rendu,
                    image_url=image_url
                )
            else:
                return JsonResponse({"error": "Type de bilan invalide."}, status=400)

            return JsonResponse({"message": "Bilan ajouté avec succès.", "bilan_id": bilan.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Données JSON invalides."}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Erreur inattendue : {str(e)}"}, status=500)
    return JsonResponse({"error": "Méthode non autorisée."}, status=405)


import matplotlib.pyplot as plt
import io
import os
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .models import BilanBiologique, Bilan, Consultation

def generer_graphique_bilan_biologique(request, consultation_id):
    try:
        # Récupérer les bilans actuels pour la consultation
        bilans_actuels = Bilan.objects.filter(consultation_id=consultation_id).order_by('date_emission')
        
        # Récupérer les bilans biologiques associés
        bilan_biologique_dict = {bilan.bilan_ptr_id: bilan.resultat for bilan in BilanBiologique.objects.all()}

        labels = [bilan.prescription for bilan in bilans_actuels]
        resultats_actuels = []
        resultats_precedents = []
        
        for bilan in bilans_actuels:
            resultat = bilan_biologique_dict.get(bilan.id, "0")
            if "/" in resultat:
                ancien, nouveau = resultat.split("/")
                try:
                    resultats_precedents.append(float(ancien))
                    resultats_actuels.append(float(nouveau))
                except ValueError:
                    resultats_precedents.append(0)
                    resultats_actuels.append(0)
            elif " " in resultat:
                ancien, nouveau = resultat.split(" ")
                try:
                    resultats_precedents.append(float(ancien))
                    resultats_actuels.append(float(nouveau))
                except ValueError:
                    resultats_precedents.append(0)
                    resultats_actuels.append(0)
            else:
                try:
                    resultats_actuels.append(float(resultat))
                    resultats_precedents.append(0)
                except ValueError:
                    resultats_actuels.append(0)
                    resultats_precedents.append(0)

        # Vérifier et ajuster les listes pour qu'elles aient la même longueur
        max_length = max(len(resultats_actuels), len(resultats_precedents))
        if len(resultats_actuels) < max_length:
            resultats_actuels.extend([0] * (max_length - len(resultats_actuels)))
        if len(resultats_precedents) < max_length:
            resultats_precedents.extend([0] * (max_length - len(resultats_precedents)))
        
        width = 0.35

        fig, ax = plt.subplots()
        ax.bar(labels, resultats_precedents, width, label='Précédent', color='r')
        ax.bar(labels, resultats_actuels, width, bottom=resultats_precedents, label='Actuel', color='b')

        ax.set_xlabel('Tests')
        ax.set_ylabel('Valeurs')
        ax.set_title('Comparaison des Bilans Biologiques')
        ax.legend()

        # Enregistrer le graphique sur le serveur
        image_path = os.path.join(settings.MEDIA_ROOT, f'graphique_biologique_{consultation_id}.png')
        plt.savefig(image_path, format='png')
        plt.close()

        # Utiliser le champ resume pour stocker le chemin du graphique
        consultation = Consultation.objects.get(id=consultation_id)
        consultation.resume += f'\nGraphique : /media/graphique_biologique_{consultation_id}.png'
        consultation.save()

        # Retourner le graphique directement dans la réponse HTTP
        buffer = io.BytesIO()
        with open(image_path, 'rb') as f:
            buffer.write(f.read())
        buffer.seek(0)

        return HttpResponse(buffer, content_type='image/png')

    except Exception as e:
        return JsonResponse({"error": f"Erreur inattendue : {str(e)}"}, status=500)


"""

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Consultation, BilanRadiologique

@csrf_exempt
def uploader_bilan_radiologique(request, consultation_id):
    if request.method == 'POST':
        try:
            # Extraire les données du formulaire
            compte_rendu = request.POST.get('compte_rendu', '')
            image = request.FILES.get('image')

            # Récupérer la consultation
            consultation = get_object_or_404(Consultation, id=consultation_id)

            # Créer et associer le bilan radiologique à la consultation
            bilan_radiologique = BilanRadiologique.objects.create(
                consultation=consultation,
                compte_rendu=compte_rendu,
                image_url=image
            )

            return JsonResponse({"message": "Bilan radiologique ajouté et associé à la consultation avec succès.", "bilan_id": bilan_radiologique.id}, status=201)

        except Exception as e:
            return JsonResponse({"error": f"Erreur inattendue : {str(e)}"}, status=500)
    return JsonResponse({"error": "Méthode non autorisée."}, status=405)
"""
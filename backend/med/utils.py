import qrcode 
from .models import Patient

def generate_qrcode(patient):
    # Utiliser le numéro de sécurité sociale (nss) du patient pour générer le QR code
    qr_data = f"nss:{patient.nss}"
    qr_code = qrcode.make(qr_data)
    
    # Sauvegarder le QR code en tant qu'image
    qr_code_path = f"med/qr_codes/{patient.nss}.png"
    qr_code.save(qr_code_path)
    
    return qr_code_path


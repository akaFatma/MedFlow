import qrcode 
from .models import Patient

def generate_qrcode(patient):
    # Utiliser le numéro de sécurité sociale (nss) du patient pour générer le QR code
    qr_data = f"nss:{patient.nss}"
    qr_code = qrcode.make(qr_data)
    
    # Sauvegarder le QR code en tant qu'image 
    qr_code_image = ContentFile(qr_code.tobytes(), f"{patient.nss}.png") 
    patient.qr_code_image.save(f"{patient.nss}.png", qr_code_image)
    
    return qr_code_path


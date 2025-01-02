import qrcode 
from .models import Patient
from django.core.files.base import ContentFile
from io import BytesIO


def generate_qrcode(patient):
    # Utiliser le numéro de sécurité sociale (nss) du patient pour générer le QR code
    qr_data = f"nss:{patient.nss}"
    print('qrdata:', qr_data)

     # Create the QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Convert QR code to an image
    qr_code_image = qr.make_image(fill_color="black", back_color="white")
    
    # Save the image to an in-memory buffer
    buffer = BytesIO()
    qr_code_image.save(buffer, format="PNG")
    buffer.seek(0)
    
    # Save the QR code image to the patient's `qr_code_image` field
    filename = f"{patient.nss}.png"
    patient.qr_code.save(filename, ContentFile(buffer.read()), save=True)
    print('supposed saved to ', filename)


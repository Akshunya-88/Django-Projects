from io import BytesIO
import pyotp
import qrcode
from django.http import HttpResponse
from .models import UserOTP
from django.conf import settings

def generate_qr_code(user):
    otp_secret = pyotp.random_base32()
    user_otp, created = UserOTP.objects.get_or_create(user=user, defaults={'otp_secret': otp_secret})

    if not created:
        # If the record already exists, update the otp_secret
        user_otp.otp_secret = otp_secret
        user_otp.save()  
    totp = pyotp.TOTP(user_otp.otp_secret,interval=60)
    otp = totp.now()
    print(otp)
    otp_uri = totp.provisioning_uri(user.username, issuer_name=settings.OTP_ISSUER_NAME)

    # Generate QR code
    qr = qrcode.QRCode(box_size=10, border=5)
    qr.add_data(otp_uri)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    return HttpResponse(buffer, content_type='image/png')

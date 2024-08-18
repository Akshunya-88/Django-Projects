from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import *
from .utils import *

class QRCodeView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_description="Get the QR code for enabling two-factor authentication",
        responses={200: openapi.Response("QR Code URL", schema=openapi.Schema(type=openapi.TYPE_STRING))}
    )
    def get(self, request):
        user = request.user  # Assuming you have a logged-in user
        qr_code_image = generate_qr_code(user)
        return qr_code_image
    
@swagger_auto_schema(
    method='post',
    operation_description="Verify the OTP provided by the user",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'otp': openapi.Schema(type=openapi.TYPE_STRING, description='One-time password'),
        }
    ),
    responses={
        200: openapi.Response("OTP is valid"),
        400: openapi.Response("Invalid OTP"),
    }
)
@api_view(['POST'])
def verify_otp(request):
    otp = request.data.get('otp')
    user = request.user
    user_otp = UserOTP.objects.get(user=user)
    totp = pyotp.TOTP(user_otp.otp_secret)
    is_valid=totp.verify(otp,valid_window=1)
    if is_valid:
        return Response({"message": "OTP is valid"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

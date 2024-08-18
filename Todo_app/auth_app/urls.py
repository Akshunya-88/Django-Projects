from django.urls import path
from .views  import *

urlpatterns = [
    path('qr-code/', QRCodeView.as_view(), name='qr-code'),
    path('verify-otp/', verify_otp, name='verify-otp'),
    # Add other URLs
]
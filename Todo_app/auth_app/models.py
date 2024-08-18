from django.db import models
from django.contrib.auth.models import User
import pyotp

class UserOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_secret = models.CharField(max_length=16, unique=True)


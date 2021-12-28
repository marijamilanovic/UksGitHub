from django.contrib.auth.models import User

from django.db import models

ADMINISTRATOR = "Administrator"
AUTHENTICATE_USER = "Authenticate user"
UNAUTHENTICATE_USER = "Unauthenticate user"
ROLE_TYPE = [
    (ADMINISTRATOR, "Administrator"),
    (AUTHENTICATE_USER, "Authenticate user"),
    (UNAUTHENTICATE_USER, "Unauthenticate user")
]

class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role =  models.CharField(max_length=20, choices=ROLE_TYPE, default=UNAUTHENTICATE_USER)

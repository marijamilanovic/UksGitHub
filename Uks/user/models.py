from django.db import models

ADMINISTRATOR = "Administrator"
AUTHENTICATE_USER = "Authenticate user"
UNAUTHENTICATE_USER = "Unauthenticate user"
ROLE_TYPE = [
    (ADMINISTRATOR, "Administrator"),
    (AUTHENTICATE_USER, "Authenticate user"),
    (UNAUTHENTICATE_USER, "Unauthenticate user")
]

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    role =  models.CharField(max_length=20, choices=ROLE_TYPE, default=UNAUTHENTICATE_USER)

from django.db import models

from user.models import User

class Comment(models.Model):
    author = models.ForeignKey(to=User, null=True, on_delete=models.CASCADE)
    content = models.TextField(default='', blank= True)

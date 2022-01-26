from django.db import models
from colorfield.fields import ColorField
from repository.models import Repository

class Label(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='', blank= True)
    color = ColorField(format='hexa')
    repository = models.ForeignKey(to=Repository, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
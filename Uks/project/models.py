from django.db import models
from repository.models import Repository

class Project(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.TextField(default='', blank= True)
    repository = models.ForeignKey(to=Repository, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

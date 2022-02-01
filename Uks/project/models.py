from django.db import models
from repository.models import Repository

OPENED = "Opened"
CLOSED = "Closed"
PROJECT_STATUS = [
    (OPENED, "Opened"),
    (CLOSED, "Closed")
]

class Project(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.TextField(default='', blank= True)
    repository = models.ForeignKey(to=Repository, null=False, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=PROJECT_STATUS, default=OPENED)

    def __str__(self):
        return self.name

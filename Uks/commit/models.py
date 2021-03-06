from django.db import models
from django.utils import timezone

from datetime import datetime, timezone
from repository.models import Repository

from branch.models import Branch
from django.contrib.auth.models import User

OPENED = "Opened"
CLOSE = "Close"
ISSUE_STATE = [
    (OPENED, "Opened"),
    (CLOSE, "Close")
]

class Commit(models.Model):
    message =  models.TextField(default='', blank= True)
    date_time = models.DateTimeField()
    hash_id = models.CharField(max_length=100)
    branch = models.ForeignKey(to=Branch, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    repository = models.ForeignKey(to=Repository, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.message

from django.db import models

from pullrequest.models import Pullrequest
from repository.models import Repository

OPENED = "Opened"
CLOSE = "Close"
ISSUE_STATE = [
    (OPENED, "Opened"),
    (CLOSE, "Close")
]

class Issue(models.Model):
    issue_title = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=50, default='')
    state = models.CharField(max_length=20, choices=ISSUE_STATE, default=OPENED)
    repository = models.ForeignKey(to=Repository, on_delete=models.CASCADE)
    pullrequests = models.ManyToManyField(Pullrequest)
    
    def __str__(self):
        return self.issue_title

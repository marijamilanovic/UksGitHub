from django.db import models

from task.models import Task
from pullrequest.models import Pullrequest

OPENED = "Opened"
CLOSE = "Close"
ISSUE_STATE = [
    (OPENED, "Opened"),
    (CLOSE, "Close")
]

class Issue(Task):
    issue_title = models.CharField(max_length=50)
    state = models.CharField(max_length=20, choices=ISSUE_STATE, default=OPENED)
    pullrequests = models.ManyToManyField(Pullrequest)
    description = models.CharField(max_length=50)
    
    def __str__(self):
        return self.issue_title

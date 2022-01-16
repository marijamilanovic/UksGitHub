from django.db import models
from django.utils import timezone

from datetime import datetime, timezone
from project.models import Project
from repository.models import Repository

OPENED = "Opened"
CLOSED = "Closed"
MILESTONE_STATUS = [
    (OPENED, "Opened"),
    (CLOSED, "Closed")
]

class Milestone(models.Model):
    title = models.CharField(max_length=50, default='')
    description = models.TextField(default='', blank= True)
    status = models.CharField(max_length=20, choices=MILESTONE_STATUS, default=OPENED)
    created = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    project = models.ForeignKey(to=Project, null=True, on_delete=models.CASCADE)
    repository = models.ForeignKey(to=Repository, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

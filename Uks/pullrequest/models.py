from django.db import models
from django.utils import timezone

from datetime import datetime, timezone
from task.models import Task
from branch.models import Branch
from comment.models import Comment
from repository.models import Repository
from django.contrib.auth.models import User

OPENED = "Opened"
CLOSED = "Closed"
MERGED = "Merged"
PULL_REQUEST_STATE = [
    (OPENED, "Opened"),
    (CLOSED, "Closed"),
    (MERGED, "Merged")
]

class Pullrequest(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=PULL_REQUEST_STATE, default=OPENED)
    created = models.DateField(null=True, blank=True)
    prRepository = models.ForeignKey(to=Repository, null=True, on_delete=models.CASCADE)
    #prRepository = models.ForeignKey(to=Repository, null=True, on_delete=models.DO_NOTHING)
    source = models.ForeignKey(to=Branch, related_name='source_branch', null=True, on_delete=models.CASCADE)
    target = models.ForeignKey(to=Branch, related_name='target_branch', null=True, on_delete=models.CASCADE)
    comments = models.ManyToManyField(Comment)
    creator = models.ForeignKey(to=User, null=True, on_delete=models.CASCADE)
    reviewers = models.ManyToManyField(User,related_name='pullrequest_reviewers')
    reviewed = models.BooleanField(default=False)
    def __str__(self):
        return self.name

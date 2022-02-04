from django.db import models

from pullrequest.models import Pullrequest
from project.models import Project
from repository.models import Repository
from milestone.models import Milestone
from label.models import Label;
from django.contrib.auth.models import User
from history.models import History
from comment.models import Comment

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
    opened_by = models.CharField(max_length=50, default='')
    assignees = models.ManyToManyField(User, related_name='user_assignees')
    projects = models.ManyToManyField(Project)
    repository = models.ForeignKey(to=Repository, on_delete=models.CASCADE)
    pullrequests = models.ManyToManyField(Pullrequest)
    milestone = models.ForeignKey(to=Milestone,null=True, on_delete=models.CASCADE)
    labels = models.ManyToManyField(Label)
    created = models.DateField(null=True, blank=True)
    history = models.ManyToManyField(History)
    comments = models.ManyToManyField(Comment)
    
    
    def __str__(self):
        return self.issue_title

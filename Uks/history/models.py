from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, timezone

MILESTONE = "Milestone"
ISSUE = "Issue"
PROJECT = "Project"
PULL_REQUEST = "Pull request"
LABEL = "Label"
ASSIGNEES = "Assignees"
CHANGES = "Changes"
COMMENTS = "Comments"
APPROVED = "Approved"
MERGED = "Merged"

OBJECT_TYPE = [
    (MILESTONE, "Milestone"),
    (ISSUE, "Issue"),
    (PROJECT, "Project"),
    (PULL_REQUEST, "Pull request"),
    (LABEL, "Label"),
    (ASSIGNEES, "Assignees"),
    (CHANGES, "Changes"),
    (COMMENTS, "Comments"),
    (APPROVED, "Approved"),
    (MERGED, "Merged")
]

class History(models.Model):
    user = models.ForeignKey(to=User, null=True, on_delete=models.CASCADE)
    message = models.TextField(default='', blank= True)
    created_date = models.DateTimeField(null=True, blank=True) 
    changed_object_id = models.IntegerField(null=False)
    object_type = models.CharField(max_length=20, choices=OBJECT_TYPE, default=CHANGES)


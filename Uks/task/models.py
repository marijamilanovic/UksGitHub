from django.db import models
from django.utils import timezone

from datetime import datetime, timezone

from milestone.models import Milestone
from user.models import User

class Task(models.Model):
    task_title = models.CharField(max_length=50, default=' ')
    opened = models.DateField(auto_now_add=True)
    closed = models.DateField(null=True, blank=True)
    milestone = models.ForeignKey(to=Milestone, null=True, blank=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(to=User, null=True, on_delete=models.CASCADE, related_name='author')
    assigned = models.ManyToManyField(User)

    def __str__(self):
        return self.task_title

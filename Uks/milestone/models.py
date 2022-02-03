from django.db import models
from django.utils import timezone
from datetime import date

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

    def get_completed_percentage(self):
        issues_count = self.issue_set.count()
        if issues_count == 0:
            return 0
        closed_issues_count = self.issue_set.filter(state='Close').count()
        percentage = (closed_issues_count * 100) / issues_count
        return round(percentage)
    
    def get_closed_issues_number(self):
        return self.issue_set.filter(state='Close').count()

    def get_opened_issues_number(self):
        return self.issue_set.filter(state='Opened').count()

    def due_date_passed(self):
        if (self.due_date == None):
            return False
        if(date.today() >= self.due_date):
            return True
        return False
    
    def passed_days_count(self):
        passed_by = date.today() - self.due_date
        return passed_by.days
    


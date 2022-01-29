from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth.models import User

PUBLIC = "Public"
PRIVATE = "Private"
REPOSITORY_STATUS = [
    (PUBLIC, "Public"),
    (PRIVATE, "Private")
]

class Repository(models.Model):
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=REPOSITORY_STATUS, default=PRIVATE)
    creator = models.ForeignKey(User, null=True, related_name='user_creator', on_delete=models.CASCADE)
    developers = models.ManyToManyField(User, related_name='user_developers')
    watchers = models.ManyToManyField(User, related_name='user_watchers')
    stargazers = models.ManyToManyField(User, related_name='user_stargazers')
    forks = models.ManyToManyField(User, related_name='user_forks')

    def __str__(self):
        return self.name

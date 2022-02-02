from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

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

    def get_closed_projects_number(self):
        return self.project_set.filter(status='Closed').count()

    def get_opened_projects_number(self):
        return self.project_set.filter(status='Opened').count()

    def get_watchers_number(self):
        return self.watchers.count()

    def get_forks_number(self):
        return self.forks.count()

    def get_stargazers_number(self):
        return self.stargazers.count()

    def is_repo_forked(self):
        repos_with_same_name = Repository.objects.all().filter(name = self.name)
        forkersRepo = User.objects.all().filter(user_forks = self)
        forked_from = None
        forked_repo = None
        for f in forkersRepo:
            if (f.id == self.creator.id):
                for r in repos_with_same_name:
                    if (r.creator.id != self.creator.id):
                        forked_repo = r
                        forked_from = get_object_or_404(User, id=r.creator.id)
                        break
                    else:
                        forked_from = get_object_or_404(User, id=r.creator.id)
            else:
                if (f.id != self.creator.id):
                    for r in repos_with_same_name:
                        if (r.creator.id != self.creator.id): 
                            forked_from = get_object_or_404(User, id=r.creator.id)
                            forked_repo = r
                        else: 
                            forked_from = get_object_or_404(User, id=r.creator.id)
                            forked_repo = repository
                            break

        return forked_from, forked_repo


    

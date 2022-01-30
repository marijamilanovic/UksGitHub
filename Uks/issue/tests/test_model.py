from django.test import TestCase
from django.contrib.auth.models import User
from issue.views import get_milestones_by_repo,  get_users_by_repo, get_issue_by_id, get_projects_by_repo, get_milestones_by_issue_repo, get_pullrequests_by_repo
from repository.models import Repository
from django.urls import reverse
from issue.models import Issue as Iss
from milestone.models import Milestone
from datetime import date
from project.models import Project
from pullrequest.models import Pullrequest

class IssueModelTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser1')
        repository = Repository.objects.create(id= 1, name='Repo1', status='public', creator = user)
        collaborator1 = User.objects.create(id=1, username='collaborator1')
        repository.developers.add(collaborator1)
        Iss.objects.create(id='1', issue_title='Issue', description = 'TestIssue', repository = repository)
        Milestone.objects.create(id = 1, title = 'Milestone1', description = 'first milestone', status = 'Opened', created=date.today(), due_date=date.today(), repository = repository)
        Project.objects.create(id = 1, name = 'project1', repository = repository)
        Pullrequest.objects.create(id = 1, prRepository = repository)

    def test_issue_description(self):
        issue = Iss.objects.get(id=1)
        issue_description = issue._meta.get_field('description').verbose_name
        self.assertEquals(issue_description, 'description')
    
    def test_issue_milestone(self):
        issue = Iss.objects.get(id=1)
        milestone = issue._meta.get_field('milestone').verbose_name
        self.assertEquals(milestone, 'milestone')
    
    def test_get_users_by_repo(self):
        repository = Repository.objects.get(id = 1)
        self.assertEquals(len(get_users_by_repo(repository)), 1)
    
    def test_get_milestones_by_repo(self):
        repository = Repository.objects.get(id = 1)
        self.assertEquals(len(get_milestones_by_repo(repository.id)), 1)
    
    def test_get_projects_by_repo(self):
        repository = Repository.objects.get(id = 1)
        self.assertEquals(len(get_projects_by_repo(repository)), 1)
    
    def test_get_milestones_by_issue_repo(self):
        issue = Iss.objects.get(id = 1)
        repository = issue.repository
        self.assertEquals(len(get_milestones_by_issue_repo(repository.id)), 1)
    
    def test_get_pullrequests_by_repo(self):
        repository = Repository.objects.get(id = 1)
        self.assertEquals(len(get_pullrequests_by_repo(repository)), 1)
    
    def test_get_issue_by_id(self):
        self.assertTrue(get_issue_by_id(1))
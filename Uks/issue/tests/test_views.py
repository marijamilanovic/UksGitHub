from sqlite3 import PrepareProtocol
from django.test import TestCase, Client
from django.contrib.auth.models import User
from repository.models import Repository
from django.urls import reverse
from issue.models import Issue as Iss
from milestone.models import Milestone
from datetime import date
from project.models import Project
from pullrequest.models import Pullrequest

class Issue(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser1')
        user.set_password('testuser1')
        user.save()
        client = Client()
        client.login(username='testuser1', password='testuser1')
        # create repository
        repository = Repository.objects.create(id= 1, name='Repo1', status='public', creator = user)
        repository.save()
        # add collaborators
        collaborator1 = User.objects.create(id=1, username='collaborator1')
        repository.developers.add(collaborator1)
        collaborator2 = User.objects.create(id=2, username='collaborator2')
        repository.developers.add(collaborator2)
        # create milestone
        Milestone.objects.create(id = 1, title = 'Milestone1', description = 'first milestone', status = 'Opened', created=date.today(), due_date=date.today(), repository = repository)
        # create projects
        Project.objects.create(id = 1, name = 'project1', repository = repository)
        Project.objects.create(id = 2, name = 'project2', repository = repository)
        # create pullrequests
        Pullrequest.objects.create(id = 1, prRepository = repository)
        Pullrequest.objects.create(id = 2, prRepository = repository)
        # create issue
        Iss.objects.create(id=11, issue_title='Issue1', repository=repository)


    def test_add_issue(self):
        # get collaborators
        assignees = []
        assignees.append(User.objects.get(id=1).username)
        assignees.append(User.objects.get(id=2).username)
        # get projects
        projects_ids = []
        projects = Project.objects.all()
        for proj in projects:
            projects_ids.append(proj.id)
        # get pullrequeests
        pullrequests_ids = []
        pullrequests = Pullrequest.objects.all()
        for pr in pullrequests:
            pullrequests_ids.append(pr.id)
        data = {
            'title': 'Issue1', 
            'description':'first issue',
            'repository': 1,
            'milestone_id': 1,
            'developers': assignees,
            'projects_ids': projects_ids,
            'pullrequests_ids': pullrequests_ids
            }
        response = self.client.post(reverse('add_issue'), data, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_view_issue(self):
        issue = Iss.objects.get(issue_title='Issue1')
        data = {}
        response = self.client.post(reverse('view_issue', kwargs={'id': issue.id}), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('milestones' in response.context)
        self.assertTrue('developers' in response.context)
        self.assertTrue('projects' in response.context)
        self.assertTrue('pullrequests' in response.context)
        self.assertEqual(len(response.context['milestones']), 1)
        self.assertEqual(len(response.context['developers']), 2)
        self.assertEqual(len(response.context['projects']), 2)
        self.assertEqual(len(response.context['pullrequests']), 2)
    
    def test_all_issues(self):
        data = {}
        response = self.client.post(reverse('all_issues'), data, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_all_issues_by_repository(self):
        data = {}
        response = self.client.post(reverse('issues', kwargs={'id': 1}), data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_update_issue(self):
        issue = Iss.objects.get(id = 11)
        issue.issue_title = 'UpdatedTitle'
        issue.description = 'UpdatedDescription'
        # get collaborators
        assignees = []
        assignees.append(User.objects.get(id=1).username)
        # get projects
        projects_ids = []
        projects = Project.objects.all()
        for proj in projects:
            projects_ids.append(proj.id)
        # get pullrequeests
        pullrequests_ids = []
        pullrequests = Pullrequest.objects.all()
        for pr in pullrequests:
            pullrequests_ids.append(pr.id)
        data = {
            'title': issue.issue_title, 
            'description': issue.description,
            'state': 'Close',
            'milestone_id': 1,
            'developers': assignees,
            'projects_ids': projects_ids,
            'pullrequests_ids': pullrequests_ids
            }
        response = self.client.post(reverse('update_issue', kwargs={'id': issue.id}),data, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_issue(self):
        issue = Iss.objects.get(id = 11)
        data = {}
        response = self.client.post(reverse('delete_issue', kwargs={'id': issue.id}),data, follow=True)
        self.assertEqual(response.status_code, 200)


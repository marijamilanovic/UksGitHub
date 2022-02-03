from django.test import TestCase, Client
from milestone.models import Milestone
from pullrequest.models import Pullrequest
from pullrequest.views import pullrequests
from repository.models import Repository
from django.contrib.auth.models import User
from label.models import Label
from issue.models import Issue
from project.models import Project
from datetime import datetime, timezone, date, timedelta
from django.urls import reverse

def fill_test_db():
        # Create users
        user = User.objects.create(username='testuser1')
        user.set_password('testuser1')
        user.save()
        client = Client()
        client.login(username='testuser1', password='testuser1')
        test_user = User.objects.create_user(username='username', password='password')
        test_user1 = User.objects.create_user(username='username1', password='password1')
        test_user2 = User.objects.create_user(username='username2', password='password2')
        test_user3 = User.objects.create_user(id = 3, username='username3', password='password3')
        test_user4 = User.objects.create_user(id = 4, username='username4', password='password4')
        test_user.save()
        test_user1.save()
        test_user2.save()
        test_user3.save()
        test_user4.save()

        # Create repositories
        test_repository = Repository.objects.create(name='repository', status='Public', creator= test_user )
        test_repository1 = Repository.objects.create(name='repository1', status='Public', creator= test_user1 )
        test_repository2 = Repository.objects.create(name='repository2', status='Private', creator= test_user2 )
        test_repository.save()
        test_repository1.save()
        test_repository2.save()

        #Pull requests
        pullrequest = Pullrequest.objects.create(id = 1, name='master', status='Opened', creator= test_user, reviewed = True)
        pullrequest2 = Pullrequest.objects.create(id = 2, name='develop1', status='Opened', creator= test_user, reviewed = True)
        pullrequest3 = Pullrequest.objects.create(id = 3, name='develop2', status='Opened', creator= test_user, reviewed = True)
        pullrequest.prRepository = test_repository
        pullrequest.reviewers.add(user)
        pullrequest3.assignees.add(test_user3)
        pullrequest2.save()
        pullrequest.save()
        pullrequest3.save()

        # Create labels
        test_label = Label.objects.create(name='bug', description='label bug', repository= test_repository )
        test_label1 = Label.objects.create(name='duplicate', description='label description', repository= test_repository1 )
        test_label.save()
        test_label1.save()

        # Create milestones
        test_milestone = Milestone.objects.create(title='Milestone', description='First milestone', repository= test_repository )
        test_milestone1 = Milestone.objects.create(title='Milestone1', description='Second milestone', repository= test_repository )
        test_milestone.save()
        test_milestone1.save()

        # Create issues
        test_issues = Issue.objects.create(issue_title='Issue', repository=test_repository)
        test_issues1 = Issue.objects.create(issue_title='Issue1', repository=test_repository)
        test_issues.save()
        test_issues1.save()

        # Create project
        test_project = Project.objects.create(name='Project1', description='first project', repository = test_repository)
        test_project1 = Project.objects.create(name='Project2', description='second project', repository = test_repository)
        test_project.save()
        test_project1.save()



class PullrequestViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        fill_test_db()

    def test_approve(self):
        client = Client()
        client.login(username='testuser1', password='testuser1')
        pullrequest = Pullrequest.objects.get(name = 'master')
        response = client.post(reverse('approve', kwargs={'pullrequest_id': pullrequest.id}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_merge(self):
        client = Client()
        client.login(username='testuser1', password='testuser1')
        pullrequest = Pullrequest.objects.get(id = 1)
        response = client.post(reverse('merge', kwargs={'pullrequest_id': pullrequest.id}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_add_assignees_on_pull_request(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='testuser', password='12345')

        pullrequest = Pullrequest.objects.get(id = 3)
        pullrequest.prRepository = Repository.objects.get(name='repository')
        pullrequest.save()
        assignees = []
        assignees.append(User.objects.get(username='username3').username)
        assignees.append(User.objects.get(username='username4').username)
        data = {'assignees': assignees}
        response = client.post(reverse('add_assignes_on_pull_request', kwargs={'id': pullrequest.id}), data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_assignees_on_pull_request(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='testuser', password='12345')

        pullrequest = Pullrequest.objects.get(name='develop2')
        pullrequest.prRepository = Repository.objects.get(name='repository')
        pullrequest.save()
        assignees_id = User.objects.get(username='username3').id
        
        response = client.post(reverse('delete_assignees_on_pull_request', kwargs={'id': pullrequest.id, 'assignee_id': assignees_id}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_add_labels_on_pull_request(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='testuser', password='12345')

        pullrequest = Pullrequest.objects.get(name='develop2')
        pullrequest.prRepository = Repository.objects.get(name='repository')
        pullrequest.save()
        labels = []
        labels.append(Label.objects.get(name='bug').id)
        labels.append(Label.objects.get(name='duplicate').id)
        data = {'labels': labels}
        response = client.post(reverse('add_labels_on_pull_request', kwargs={'id': pullrequest.id}), data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_labels_on_pull_request(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='testuser', password='12345')

        pullrequest = Pullrequest.objects.get(name='develop2')
        pullrequest.prRepository = Repository.objects.get(name='repository')
        pullrequest.save()
        label_id = Label.objects.get(name='duplicate').id
        
        response = client.post(reverse('delete_labels_on_pull_request', kwargs={'id': pullrequest.id, 'label_id': label_id}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_add_milestones_on_pull_request(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='testuser', password='12345')

        pullrequest = Pullrequest.objects.get(name='develop2')
        pullrequest.prRepository = Repository.objects.get(name='repository')
        pullrequest.save()
        milestones = []
        milestones.append(Milestone.objects.get(title='Milestone').id)
        milestones.append(Milestone.objects.get(title='Milestone1').id)
        data = {'milestones': milestones}
        response = client.post(reverse('add_milestones_on_pull_request', kwargs={'id': pullrequest.id}), data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_add_issues_on_pull_request(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='testuser', password='12345')

        pullrequest = Pullrequest.objects.get(name='develop2')
        pullrequest.prRepository = Repository.objects.get(name='repository')
        pullrequest.save()
        issues = []
        issues.append(Issue.objects.get(issue_title='Issue').id)
        issues.append(Issue.objects.get(issue_title='Issue1').id)
        data = {'issues': issues}
        response = client.post(reverse('add_issues_on_pull_request', kwargs={'id': pullrequest.id}), data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_issues_on_pull_request(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='testuser', password='12345')

        pullrequest = Pullrequest.objects.get(name='develop2')
        pullrequest.prRepository = Repository.objects.get(name='repository')
        pullrequest.save()
        issue_id = Issue.objects.get(issue_title='Issue1').id
        
        response = client.post(reverse('delete_issues_on_pull_request', kwargs={'id': issue_id, 'pr_id': pullrequest.id}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_add_issues_on_pull_request(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='testuser', password='12345')

        pullrequest = Pullrequest.objects.get(name='develop2')
        pullrequest.prRepository = Repository.objects.get(name='repository')
        pullrequest.save()
        projects = []
        projects.append(Project.objects.get(name='Project1').id)
        projects.append(Project.objects.get(name='Project2').id)
        data = {'projects': projects}
        response = client.post(reverse('add_issues_on_pull_request', kwargs={'id': pullrequest.id}), data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_projects_on_pull_request(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='testuser', password='12345')

        pullrequest = Pullrequest.objects.get(name='develop2')
        pullrequest.prRepository = Repository.objects.get(name='repository')
        pullrequest.save()
        project_id = Project.objects.get(name='Project2').id
        
        response = client.post(reverse('delete_projects_on_pull_request', kwargs={'id': pullrequest.id, 'project_id': project_id}), follow=True)
        self.assertEqual(response.status_code, 200)
    
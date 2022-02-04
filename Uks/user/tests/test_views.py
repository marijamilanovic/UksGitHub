from django.test import TestCase
from milestone.models import Milestone
from repository.models import Repository
from django.contrib.auth.models import User
from issue.models import Issue
from datetime import datetime, timezone, date, timedelta
from django.urls import reverse
from project.models import Project

def fill_test_db():
        # Create users
        test_user = User.objects.create_user(username='username', password='password')
        test_user1 = User.objects.create_user(username='username1', password='password1')
        test_user2 = User.objects.create_user(username='username2', password='password2')
        test_user.save()
        test_user1.save()
        test_user2.save()

        # Create repositories
        test_repository = Repository.objects.create(name='repository', status='public', creator= test_user )
        test_repository1 = Repository.objects.create(name='repository1', status='public', creator= test_user1 )
        test_repository2 = Repository.objects.create(name='repository2', status='private', creator= test_user2 )
        test_repository.save()
        test_repository1.save()
        test_repository2.save()

        # Create milestones
        test_milestone = Milestone.objects.create(title='Milestone1', description='first milestone',status='Opened',created=date.today(),due_date=date.today(),repository = test_repository)
        test_milestone1 = Milestone.objects.create(title='Milestone2', description='second milestone',status='Opened',created=date.today(),due_date=date.today(),repository = test_repository1)
        test_milestone2 = Milestone.objects.create(title='Milestone3', description='third milestone',status='Opened',created=date.today(),due_date=date.today(),repository = test_repository)
        test_milestone.save()
        test_milestone1.save()
        test_milestone2.save()

        # Create issues
        test_issue = Issue.objects.create(issue_title='Issue1', description='first issue',state='Opened',opened_by= test_user.username , repository = test_repository,milestone = test_milestone)
        test_issue1 = Issue.objects.create(issue_title='Issue2', description='second issue',state='Opened',opened_by= test_user.username, repository = test_repository1,milestone = test_milestone)
        test_issue2 = Issue.objects.create(issue_title='Issue3', description='third issue',state='Close',opened_by= test_user1.username, repository = test_repository,milestone = test_milestone1)
        test_issue.save()
        test_issue1.save()
        test_issue2.save()

        # Create projects
        test_project = Project.objects.create(name='Project1', description='first project', repository = test_repository)
        test_project1 = Project.objects.create(name='Project2', description='second project', repository = test_repository)
        test_project2 = Project.objects.create(name='Project3', description='third project', repository = test_repository1)
        test_project.save()
        test_project1.save()
        test_project2.save()


class UserViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        fill_test_db()

    def test_search(self):
        credentials = {'username': 'username', 'password': 'password'}
        response = self.client.post(reverse('login'), credentials, follow=True)
        searchedWord = ['repository']
        data = {'search': searchedWord}
        response = self.client.post(reverse('search'),data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['repositories']), 2)  

    def test_user_projects(self):
        user = User.objects.get(username='username')
        response = self.client.get(reverse('user_projects', kwargs={'id': user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('projects' in response.context)
        self.assertEqual(len(response.context['projects']), 2)

    
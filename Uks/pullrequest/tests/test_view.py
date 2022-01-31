from django.test import TestCase, Client
from milestone.models import Milestone
from pullrequest.models import Pullrequest
from pullrequest.views import pullrequests
from repository.models import Repository
from django.contrib.auth.models import User
from issue.models import Issue
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
        test_user.save()
        test_user1.save()
        test_user2.save()

        # Create repositories
        test_repository = Repository.objects.create(name='repository', status='Public', creator= test_user )
        test_repository1 = Repository.objects.create(name='repository1', status='Public', creator= test_user1 )
        test_repository2 = Repository.objects.create(name='repository2', status='Private', creator= test_user2 )
        test_repository.save()
        test_repository1.save()
        test_repository2.save()

        #Pull requests
        pullrequest = Pullrequest.objects.create(id = 1, name='master', status='Opened', creator= test_user, reviewed = True)
        pullrequest2 = Pullrequest.objects.create(id = 2, name='develop', status='Opened', creator= test_user, reviewed = True)
        pullrequest.prRepository = test_repository
        pullrequest.reviewers.add(user)
        pullrequest2.save()
        pullrequest.save()

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

    

    
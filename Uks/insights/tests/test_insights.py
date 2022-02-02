from ast import arg
from django.test import TestCase, Client
from django.urls import reverse, resolve
from repository.models import PRIVATE, Repository
from django.contrib.auth.models import User
from branch.models import Branch
from commit.models import Commit
from datetime import datetime, timedelta
from pullrequest.models import Pullrequest
from issue.models import Issue, OPENED
from branch.views import createBranch



class TestInsigths(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(username="user1")
        user1.set_password('user1')
        user1.save()
        user2 = User.objects.create(username="user2")
        user2.set_password('user2')
        user2.save()
        repo = Repository.objects.create(name="repo", status=PRIVATE, creator=user1)
        repo.developers.add(user1)
        repo.developers.add(user2)
        Branch.objects.create(name="master", is_default=True, repository=repo)
        develop = Branch.objects.create(name="develop", is_default=False, repository=repo)
        Commit.objects.create(message="First commit", date_time=(datetime.now() - timedelta(days=4)), hash_id="ds7fgs4", branch=develop, author=user1, repository = repo)
        Commit.objects.create(message="First commit1", date_time=datetime.now(), hash_id="ds7fgs4", branch=develop, author=user2, repository=repo)

        Pullrequest.objects.create(id = 1, prRepository = repo, created=datetime.now())
        Pullrequest.objects.create(id = 2, prRepository = repo, created=datetime.now())
        
        Issue.objects.create(id=11, issue_title='Issue1', repository=repo, state=OPENED, created=datetime.now())

    def setUp(self) -> None:
        self.client = Client()

    def test_pulse_tab(self):
        credentials = {}

        repo = Repository.objects.get(name='repo')

        id = repo.id

        self.client.login(username='user1', password='user1')

        response = self.client.get(reverse('insights:pulse', args=[repo.id, 3]), credentials, follow=True)

        self.assertEqual(response.context['open_is'], 1)
        self.assertEqual(response.status_code, 200)


    def test_pulse_tab2(self):
        credentials = {}

        repo = Repository.objects.get(name='repo')

        id = repo.id

        self.client.login(username='user1', password='user1')

        response = self.client.get(reverse('insights:pulse', args=[repo.id, 3]), credentials, follow=True)

        self.assertFalse(response.context['closed_is'], 1)

    def test_pulse_tab_pr(self):
        credentials = {}

        repo = Repository.objects.get(name='repo')

        id = repo.id

        self.client.login(username='user1', password='user1')

        response = self.client.get(reverse('insights:pulse', args=[repo.id, 3]), credentials, follow=True)

        self.assertEqual(response.context['open_pr'], 2)
        self.assertEqual(response.status_code, 200)

    def test_pulse_tab_pr2(self):
        credentials = {}

        repo = Repository.objects.get(name='repo')

        id = repo.id

        self.client.login(username='user1', password='user1')

        response = self.client.get(reverse('insights:pulse', args=[repo.id, 3]), credentials, follow=True)

        self.assertFalse(response.context['closed_pr'], 3)

    def test_contributors(self):
        credentials = {}

        repo = Repository.objects.get(name='repo')

        id = repo.id

        self.client.login(username='user1', password='user1')

        response = self.client.get(reverse('insights:contributors', args=[repo.id, 3]), credentials, follow=True)

        self.assertEqual(response.context['data'][0], 1)
        self.assertEqual(response.status_code, 200)

    def test_contributors2(self):
        credentials = {}

        repo = Repository.objects.get(name='repo')

        id = repo.id

        self.client.login(username='user1', password='user1')

        response = self.client.get(reverse('insights:contributors', args=[repo.id, 7]), credentials, follow=True)

        self.assertEqual(response.context['data'][0], 1)
        self.assertEqual(response.context['data'][4], 1)

        self.assertEqual(response.status_code, 200)

    def test_commits(self):
        credentials = {}

        repo = Repository.objects.get(name='repo')

        self.client.login(username='user1', password='user1')

        id = repo.id

        response = self.client.get(reverse('insights:commits', args=[repo.id]), credentials, follow=True)

        self.assertEqual(response.context['data7'][0], 1)
        self.assertEqual(response.status_code, 200)


        





        

    









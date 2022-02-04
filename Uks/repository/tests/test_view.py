from http import client
from turtle import title
from django.test import TestCase, Client
from pullrequest.models import Pullrequest
from repository.models import Repository
from branch.models import Branch
from django.contrib.auth.models import User
from comment.models import Comment
from datetime import datetime, timezone, date, timedelta
from django.urls import reverse

from repository.views import add_collaborator_on_repository, remove_collaborato_from_repository
def fill_test_db():
        # Create users
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

        # Create brances
        test_branch = Branch.objects.create(name = 'Branch1', is_default = True, repository = test_repository1)
        test_branch1 = Branch.objects.create(name = 'Branch2', is_default = False, repository = test_repository1)
        test_repository.save()
        test_repository1.save()
        test_repository2.save()

        # add developer on repository
        test_repository1.developers.add(test_user)
        test_repository1.developers.add(test_user2)

        # add watchers, stargazers and forkers on repository
        test_repository1.watchers.add(test_user)
        test_repository1.watchers.add(test_user2)
        test_repository1.stargazers.add(test_user)
        test_repository1.stargazers.add(test_user2)
        #test_repository1.forks.add(test_user)

class RepositoryViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        fill_test_db()

    def test_add_collaborator_on_repository(self):
        credentials = {'username': 'username1', 'password': 'password1'}
        self.client.post(reverse('login'), credentials, follow=True)
        developer = User.objects.get(username='username1')
        repository = Repository.objects.get(name = 'repository1')
        collaborators = add_collaborator_on_repository(repository, developer)
        self.assertEqual(len(collaborators), 3)

    def test_add_collaborator_on_repository_view(self):
        developer = User.objects.get(username='username1')
        repository = Repository.objects.get(name = 'repository1')
        response = self.client.post(reverse('add_collaborator', kwargs={'id': repository.id, 'developer_id':developer.id}), follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_remove_collaborator_from_repository(self):
        credentials = {'username': 'username1', 'password': 'password1'}
        self.client.post(reverse('login'), credentials, follow=True)
        developer = User.objects.get(username='username')
        repository = Repository.objects.get(name = 'repository1')
        collaborators = remove_collaborato_from_repository(repository, developer)
        self.assertEqual(len(collaborators), 1)

    def test_remove_collaborator_from_repository_view(self):
        credentials = {'username': 'username1', 'password': 'password1'}
        self.client.post(reverse('login'), credentials, follow=True)
        developer = User.objects.get(username='username')
        repository = Repository.objects.get(name = 'repository1')
        response = self.client.post(reverse('remove_collaborator', kwargs={'id': repository.id, 'developer_id':developer.id}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_watchers_repository(self):
        credentials = {'username': 'username1', 'password': 'password1'}
        self.client.post(reverse('login'), credentials, follow=True)
        repository = Repository.objects.get(name = 'repository1')
        response = self.client.get(reverse('watchers', kwargs={'id': repository.id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['watchers']), 2)
        self.assertTrue('repository' in response.context)

    def test_watch_repository(self):
        credentials = {'username': 'username1', 'password': 'password1'}
        self.client.post(reverse('login'), credentials, follow=True)
        repository = Repository.objects.get(name = 'repository1')
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='testuser', password='12345')
        repository.creator = user
        response = client.get(reverse('watchRepository', kwargs={'id': repository.id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['watchers']), 3)

    def test_get_stargazers_repository(self):
        credentials = {'username': 'username1', 'password': 'password1'}
        self.client.post(reverse('login'), credentials, follow=True)
        repository = Repository.objects.get(name = 'repository1')
        response = self.client.get(reverse('stargazers', kwargs={'id': repository.id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['stargazers']), 2)
        self.assertTrue('repository' in response.context)

    def test_star_repository(self):
        repository = Repository.objects.get(name = 'repository1')
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='testuser', password='12345')
        repository.creator = user
        response = client.get(reverse('starRepository', kwargs={'id': repository.id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['stargazers']), 3)

    def test_no_forkers_repository(self):
        credentials = {'username': 'username1', 'password': 'password1'}
        self.client.post(reverse('login'), credentials, follow=True)
        repository = Repository.objects.get(name = 'repository1')
        response = self.client.get(reverse('forkers', kwargs={'id': repository.id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['forks']), 0)

    def test_fork_repo(self):
        repository = Repository.objects.get(name = 'repository1')
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='testuser', password='12345')
        repository.creator = user
        response = client.get(reverse('forkRepository', kwargs={'id': repository.id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['forks']), 1)
    
    def test_get_forkers_repository(self):
        credentials = {'username': 'username1', 'password': 'password1'}
        self.client.post(reverse('login'), credentials, follow=True)
        repository = Repository.objects.get(name = 'repository1')
        user = User.objects.create_user(username='miki', password='miki')
        repository.forks.add(user)
        repo = Repository.objects.create(name='repository1', status='Public', creator= user )
        repo.save()
        response = self.client.get(reverse('forkers', kwargs={'id': repository.id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['forks']), 1)

    

        

        
    

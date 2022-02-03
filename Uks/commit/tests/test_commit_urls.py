from django.test import TestCase, Client
from django.urls import reverse, resolve
from repository.models import PRIVATE, Repository
from django.contrib.auth.models import User
from branch.models import Branch
from commit.models import Commit
from datetime import datetime



class CommitTestCase(TestCase):
    @classmethod
    def setUp(self):
        user = User.objects.create(username="user1")
        user.set_password('user1')
        user.save()
        repo = Repository.objects.create(name="repo", status=PRIVATE, creator=user)
        master = Branch.objects.create(name="master", is_default=True, repository=repo)
        develop = Branch.objects.create(name="develop", is_default=False, repository=repo)
        Commit.objects.create(message="First commit", date_time=datetime(2022,1,27), hash_id="ds7fgs4", branch=develop, author=user)
        Commit.objects.create(message="First commit1", date_time=datetime(2022,1,27), hash_id="ds7fgs4", branch=develop, author=user)

        


    def test_create_commit(self):
        credentials = {'message': 'New Commit'}

        branch = Branch.objects.get(name='develop')

        self.client.login(username='user1', password='user1')

        response = self.client.post(reverse('commit:newCommit', args=[branch.id]), credentials, follow=True)

        self.assertEqual(Commit.objects.get(message='New Commit').message, 'New Commit')
        self.assertEqual(response.status_code, 200)


    def test_commit_list(self):
        branch = Branch.objects.get(name='develop')

        self.client.login(username='user1', password='user1')

        response = self.client.post(reverse('commit:commitList', args=[branch.id]), follow=True)

        self.assertListEqual(list(response.context['commit_list']), list(Commit.objects.all().filter(branch = branch)))
        self.assertEqual(response.status_code, 200)

    def test_delete_commit(self):

        commit = Commit.objects.get(message="First commit")

        self.client.login(username='user1', password='user1')

        response = self.client.post(reverse('commit:deleteCommit', args=[commit.id]), follow=True)

        self.assertEqual(len(list(Commit.objects.all())), 1)
        self.assertEqual(response.status_code, 200)

    





   









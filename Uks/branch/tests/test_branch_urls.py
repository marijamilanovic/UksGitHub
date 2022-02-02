from ast import arg
from django.test import TestCase, Client
from django.urls import reverse, resolve
from repository.models import PRIVATE, Repository
from django.contrib.auth.models import User
from branch.models import Branch
from branch.views import createBranch



class TestBranchUrls(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="user1")
        user.set_password('user1')
        user.save()
        repo = Repository.objects.create(name="repo", status=PRIVATE, creator=user)
        Branch.objects.create(name="master", is_default=True, repository=repo)
        Branch.objects.create(name="develop", is_default=False, repository=repo)

    def setUp(self) -> None:
        self.client = Client()

    def test_create_branch(self):
        credentials = {'name': 'develop2'}

        repo = Repository.objects.get(name='repo')

        id = repo.id

        self.client.login(username='user1', password='user1')

        response = self.client.post(reverse('branch:createBranch', args=[repo.id]), credentials, follow=True)

        self.assertEqual(Branch.objects.get(name="develop2").name, "develop2")
        self.assertEqual(response.status_code, 200)

        

    def test_create_branch_with_same_name(self):
        credentials = {'name': 'develop'}

        repo = Repository.objects.get(name='repo')

        id = repo.id

        self.client.login(username='user1', password='user1')

        response = self.client.post(reverse('branch:createBranch', args=[repo.id]), credentials, follow=True)

        self.assertEqual(response.context['error_name'], True)

    def test_create_branch_with_new_name(self):
        credentials = {'name': 'develop2'}

        repo = Repository.objects.get(name='repo')

        id = repo.id

        self.client.login(username='user1', password='user1')

        response = self.client.post(reverse('branch:createBranch', args=[repo.id]), credentials, follow=True)

        self.assertEqual(Branch.objects.get(name="develop2").name, "develop2")
        self.assertEqual(response.status_code, 200)

    def test_branch_list(self):
        repo = Repository.objects.get(name='repo')

        id = repo.id

        self.client.login(username='user1', password='user1')

        response = self.client.post(reverse('branch:repoBranchList', args=[repo.id]), follow=True)

        self.assertListEqual(list(response.context['branch_list']), list(Branch.objects.all().filter(repository = repo)))
        self.assertEqual(response.status_code, 200)


    
    def test_edit_branch(self):
        credentials = {'name': 'develop2'}

        branch = Branch.objects.get(name='develop')

        self.client.login(username='user1', password='user1')

        response = self.client.post(reverse('branch:editBranch', args=[branch.id]), credentials, follow=True)

        self.assertEqual(Branch.objects.get(name="develop2").name, "develop2")
        self.assertEqual(response.status_code, 200)

    def test_edit_branch_same_name(self):
        credentials = {'name': 'master'}

        branch = Branch.objects.get(name='develop')

        self.client.login(username='user1', password='user1')

        response = self.client.post(reverse('branch:editBranch', args=[branch.id]), credentials, follow=True)


        self.assertEqual(response.context['error_name'], True)




        

    









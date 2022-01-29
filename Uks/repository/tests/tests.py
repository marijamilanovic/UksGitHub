from pyexpat import model
from django.test import TestCase, Client
from django.contrib.auth.models import User
from home.views import repository
from repository.views import add_collaborator_on_repository, remove_collaborato_from_repository
from ..models import Repository as Repo
# Create your tests here.
class Repository(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('testuser')
        user.save()
        client = Client()
        client.login(username='testuser', password='testuser')
        repo= Repo.objects.create(id = 1, name = "repo1", status = "public", creator = user)
        repo2= Repo.objects.create(id = 2, name = "repo2", status = "public", creator = user)
        developer = User.objects.create(id = 1, username = 'developer')
        repo2.developers.add(developer)

    def test_add_collaborator_on_repository(self):
        repository = Repo.objects.get(id = 1)
        developer = User.objects.get(id = 1)
        self.assertEquals(len(add_collaborator_on_repository(repository, developer)), 1)
    
    def test_remove_collaborator_from_repository(self):
        repository = Repo.objects.get(id = 2)
        developer = User.objects.get(id = 1)
        self.assertEquals(len(remove_collaborato_from_repository(repository, developer)), 0)
        

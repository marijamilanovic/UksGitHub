from django.test import TestCase, Client
from project.models import Project
from django.contrib.auth.models import User
from repository.models import Repository


class ProjectModelTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('testuser')
        user.save()
        client = Client()
        client.login(username='testuser', password='testuser')
        repo= Repository.objects.create(id = 1, name = "repo1", status = "public", creator = user)
        Project.objects.create(name='Project1', description = 'first project', repository = repo, status = "Opened" )

    def test_name_label(self):
        project = Project.objects.get(name='Project1')
        project_name = project._meta.get_field('name').verbose_name
        self.assertEquals(project_name, 'name')

    def test_description_label(self):
        project = Project.objects.get(name='Project1')
        project_description = project._meta.get_field('description').verbose_name
        self.assertEquals(project_description, 'description')

    def test_label_status(self):
        project = Project.objects.get(name='Project1')
        project_status = project._meta.get_field('status').verbose_name
        self.assertEquals(project_status, 'status')

    def test_name_max_length(self):
        project = Project.objects.get(name='Project1')
        max_length = project._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)
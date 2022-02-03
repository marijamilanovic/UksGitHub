from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from repository.models import Repository
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
        test_repository = Repository.objects.create(name='repository', status='Public', creator= test_user )
        test_repository1 = Repository.objects.create(name='repository1', status='Public', creator= test_user1 )
        test_repository2 = Repository.objects.create(name='repository2', status='Private', creator= test_user2 )
        test_repository.save()
        test_repository1.save()
        test_repository2.save()

        # Create projects
        test_project = Project.objects.create(name='Project1', description='first project', repository = test_repository)
        test_project1 = Project.objects.create(name='Project2', description='second project', repository = test_repository)
        test_project2 = Project.objects.create(name='Project3', description='third project', repository = test_repository1)
        test_project.save()
        test_project1.save()
        test_project2.save()

class ProjectViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        fill_test_db()

    def test_get_all_repo_projects(self):
        credentials = {'username': 'username', 'password': 'password'}
        response = self.client.post(reverse('login'), credentials, follow=True)
        repository = Repository.objects.get(name='repository')
        response = self.client.get(reverse('project:projects', kwargs={'id': repository.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('repository' in response.context)
        self.assertTrue('projects' in response.context)
        self.assertEqual(len(response.context['projects']), 2)

    def test_get_project_by_id(self):
        project = Project.objects.get(name='Project1')
        response = self.client.get(reverse('project:getProjectById', kwargs={'id': project.id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('repository' in response.context)
        self.assertTrue('project' in response.context)

    def test_update_project(self):
        project = Project.objects.get(name='Project1')
        project.description = 'updated project'
        repository = project.repository
        data = {'name': project.name, 'description':project.description, 'repository': repository.id}
        response = self.client.post(reverse('project:updateProject',kwargs={'id': project.id}),data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_add_project(self):
        repository = Repository.objects.get(name='repository2')
        project = Project.objects.create(name='New project', description='new description', repository = repository)
        data = {'name': project.name, 'description':project.description,'repository':repository.id}
        response = self.client.post(reverse('project:addProject'),data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_project_close(self):
        project = Project.objects.get(name='Project1')
        response = self.client.get(reverse('project:closeProject', kwargs={'id': project.id}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_project_reopen(self):
        project = Project.objects.get(name='Project1')
        response = self.client.get(reverse('project:reopenProject', kwargs={'id': project.id}), follow=True)
        self.assertEqual(response.status_code, 200)

    
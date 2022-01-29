from django.test import TestCase
from django.urls import reverse
from label.models import Label
from django.contrib.auth.models import User
from repository.models import Repository

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

        # Create labels
        test_label = Label.objects.create(name='Bug', description='Bug fix', color='#af9bfa', repository = test_repository)
        test_label1 = Label.objects.create(name='Help wanted', description='exta help', color='#af9bfa', repository = test_repository)
        test_label2 = Label.objects.create(name='Configure', description='configure needed', color='#af9bfa', repository = test_repository1)
        test_label.save()
        test_label1.save()
        test_label2.save()

class LabelViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        fill_test_db()

    def test_get_all_repo_labels(self):
        repository = Repository.objects.get(name='repository')
        response = self.client.get(reverse('labels', kwargs={'id': repository.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('repository' in response.context)
        self.assertTrue('labels' in response.context)
        self.assertEqual(len(response.context['labels']), 2)

    def test_label_delete(self):
        label = Label.objects.get(name='Bug')
        response = self.client.get(reverse('deleteLabel', kwargs={'id': label.id}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_label_by_id(self):
        label = Label.objects.get(name='Bug')
        response = self.client.get(reverse('getLabelById', kwargs={'id': label.id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('repository' in response.context)
        self.assertTrue('label' in response.context)
        self.assertTrue('color' in response.context)

    def test_update_label(self):
        label = Label.objects.get(name='Bug')
        label.description = 'Bug fix updated'
        label.color = '#0dd0b4'
        data = {'name': label.name, 'description':label.description,'color':label.color}
        response = self.client.post(reverse('editLabel',kwargs={'id': label.id}),data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_add_label(self):
        repository = Repository.objects.get(name='repository2')
        label = Label.objects.create(name='New label', description='new label description', color='#af9bfa', repository = repository)
        data = {'name': label.name, 'description':label.description,'color':label.color,'repository':repository.id}
        response = self.client.post(reverse('addLabel'),data, follow=True)
        self.assertEqual(response.status_code, 200)
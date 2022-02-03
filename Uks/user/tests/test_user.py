from ast import arg
from django.test import TestCase, Client
from django.urls import reverse, resolve
from repository.models import PRIVATE, Repository
from django.contrib.auth.models import User



class TestInsigths(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(username="user1")
        user1.set_password('user1')
        user1.save()

    def setUp(self) -> None:
        self.client = Client()


    def test_successful_login(self):
      credentials = {'username': 'user1', 'password': 'user1'}

      response = self.client.post(reverse('login'), credentials, follow=True)

      self.assertEqual(response.status_code, 200)


    def test_unsuccessful_login(self):
      credentials = {'username': 'user1', 'password': 'user1f'}

      response = self.client.post(reverse('login'), credentials, follow=True)

      self.assertEqual(response.context['ok_login'], False)






from http import client
from turtle import title
from django.test import TestCase, Client
from pullrequest.models import Pullrequest
from repository.models import Repository
from branch.models import Branch
from django.contrib.auth.models import User
from comment.models import Comment, Emoji
from datetime import datetime, timezone, date, timedelta
from django.urls import reverse
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

        # Create branchs
        test_branch = Branch.objects.create(name='develop', is_default='True', repository= test_repository )
        test_branch1 = Branch.objects.create(name='branch1', is_default='False', repository= test_repository1 )
        test_branch.save()
        test_branch1.save()

        # Create pullrequests
        test_pullrequest = Pullrequest.objects.create(name='Pullrequest1', status='Opened',created=date.today(), prRepository = test_repository, source = test_branch, target= test_branch1, creator= test_user)
        test_pullrequest1 = Pullrequest.objects.create(name='Pullrequest2', status='Opened',created=date.today(), prRepository = test_repository1, source = test_branch, target= test_branch1, creator= test_user1)
        test_pullrequest2 = Pullrequest.objects.create(name='Pullrequest2', status='Opened',created=date.today(), prRepository = test_repository2, source = test_branch, target= test_branch1, creator= test_user2)
        test_pullrequest.save()
        test_pullrequest1.save()
        test_pullrequest2.save()

        # Create comments
        test_comment = Comment.objects.create(author= test_user, content='first comment', created_date=date.today())
        test_comment1 = Comment.objects.create(author= test_user1, content='second comment', created_date=date.today())
        test_comment2 = Comment.objects.create(author= test_user2, content='third comment', created_date=date.today())
        test_comment.save()
        test_comment1.save()
        test_comment2.save()

        # Create Emojis
        test_emoji = Emoji.objects.create(name='128640')
        test_emoji1 = Emoji.objects.create(name='128077')
        test_emoji2 = Emoji.objects.create(name='127881')
        test_emoji.save()
        test_emoji1.save()
        test_emoji2.save()


class CommentViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        fill_test_db()

  
    def test_add_comment(self):
        author = User.objects.get(username='username')
        comment = Comment.objects.create(author= author, content='first_comment', created_date=date.today())
        data = {'author':author, 'content': comment.content,'created_date':comment.created_date}
        pullrequest = Pullrequest.objects.get(name='Pullrequest1')
        response = self.client.post(reverse('add_comment', kwargs={'id': pullrequest.id}), data, follow=True)
        self.assertEqual(response.status_code, 200)
        
    def test_comment_delete(self):
        comment = Comment.objects.get(content='first comment')
        pullrequest = Pullrequest.objects.get(name='Pullrequest1')
        response = self.client.get(reverse('delete_comment', kwargs={'id': comment.id, 'pr_id': pullrequest.id}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_update_comment(self):
        comment = Comment.objects.get(content='first comment')
        comment.content = 'changed content'
        pullrequest = Pullrequest.objects.get(name='Pullrequest1')
        data = {'comment_content_edit': comment.content}
        response = self.client.post(reverse('update_comment', kwargs={'id': comment.id, 'pr_id': pullrequest.id}), data, follow=True)
        self.assertEqual(response.status_code, 200)


    def test_add_emoji(self):
        emoji = Emoji.objects.create(name='128641')
        comment = Comment.objects.get(content='first comment')
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='testuser', password='12345')
        data = {'user': user, 'emoji': emoji.name}
        pullrequest = Pullrequest.objects.get(name='Pullrequest1')
        response = client.post(reverse('add_emoji', kwargs={'id': comment.id, 'pr_id': pullrequest.id}), data, follow=True)
        print(response)
        self.assertEqual(response.status_code, 200)



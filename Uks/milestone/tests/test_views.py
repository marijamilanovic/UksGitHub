from django.test import TestCase
from milestone.models import Milestone
from repository.models import Repository
from django.contrib.auth.models import User
from issue.models import Issue
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

        # Create milestones
        test_milestone = Milestone.objects.create(title='Milestone1', description='first milestone',status='Opened',created=date.today(),due_date=date.today(),repository = test_repository)
        test_milestone1 = Milestone.objects.create(title='Milestone2', description='second milestone',status='Opened',created=date.today(),due_date=date.today(),repository = test_repository1)
        test_milestone2 = Milestone.objects.create(title='Milestone3', description='third milestone',status='Opened',created=date.today(),due_date=date.today(),repository = test_repository)
        test_milestone.save()
        test_milestone1.save()
        test_milestone2.save()

        # Create issues
        test_issue = Issue.objects.create(issue_title='Issue1', description='first issue',state='Opened',opened_by= test_user.username , repository = test_repository,milestone = test_milestone)
        test_issue1 = Issue.objects.create(issue_title='Issue2', description='second issue',state='Opened',opened_by= test_user.username, repository = test_repository1,milestone = test_milestone)
        test_issue2 = Issue.objects.create(issue_title='Issue3', description='third issue',state='Close',opened_by= test_user1.username, repository = test_repository,milestone = test_milestone1)
        test_issue.save()
        test_issue1.save()
        test_issue2.save()


class MilestoneViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        fill_test_db()

    def test_milestone_issues(self):
        milestone = Milestone.objects.get(title='Milestone1')
        response = self.client.get(reverse('seeMilestone', kwargs={'id': milestone.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('issues' in response.context)
        self.assertTrue('milestone' in response.context)
        self.assertTrue('repository' in response.context)
        self.assertEqual(len(response.context['issues']), 2)

    def test_get_all_repo_milestone(self):
        repository = Repository.objects.get(name='repository')
        response = self.client.get(reverse('milestones', kwargs={'id': repository.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('repository' in response.context)
        self.assertTrue('milestones' in response.context)
        self.assertEqual(len(response.context['milestones']), 2)

    def test_milestone_delete(self):
        milestone = Milestone.objects.get(title='Milestone1')
        response = self.client.get(reverse('deleteMilestone', kwargs={'id': milestone.id}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_milestone_by_id(self):
        milestone = Milestone.objects.get(title='Milestone2')
        response = self.client.get(reverse('getMilestoneById', kwargs={'id': milestone.id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('repository' in response.context)
        self.assertTrue('milestone' in response.context)

    def test_update_milestone(self):
        milestone = Milestone.objects.get(title='Milestone2')
        milestone.description = 'Updated second milestone'
        milestone.due_date = '2022-04-23'
        data = {'title': milestone.title, 'description':milestone.description,'dueDate':milestone.due_date}
        response = self.client.post(reverse('updateMilestone',kwargs={'id': milestone.id}),data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_add_milestone(self):
        repository = Repository.objects.get(name='repository2')
        milestone = Milestone.objects.create(title='Milestone4', description='fourth milestone',status='Opened',created=date.today(),due_date=date.today()+timedelta(days=20),repository = repository) 
        data = {'title': milestone.title, 'description':milestone.description,'dueDate':milestone.due_date,'repository':milestone.repository.id}
        response = self.client.post(reverse('addMilestone'),data, follow=True)
        self.assertEqual(response.status_code, 200)
        

    
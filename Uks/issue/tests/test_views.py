from sqlite3 import PrepareProtocol
from django.test import TestCase, Client
from django.contrib.auth.models import User
from issue.views import filter_issues
from label.models import Label
from repository.models import Repository
from django.urls import reverse
from issue.models import Issue as Iss
from milestone.models import Milestone
from datetime import date
from project.models import Project
from pullrequest.models import Pullrequest
from history.models import History

class Issue(TestCase):
    def setUp(self):
        user = User.objects.create(id = 1,username='testuser1')
        user2 = User.objects.create(id = 2,username='testuser2')
        user2.set_password('testuser2')
        user.set_password('testuser1')
        user2.save()
        user.save()
        client = Client()
        client.login(username='testuser1', password='testuser1')
        # create repository
        repository = Repository.objects.create(id= 1, name='Repo1', status='public', creator = user)
        repository2 = Repository.objects.create(id= 2, name='Repo2', status='public', creator = user)
        repository2.save()
        repository.save()

        # labels
        l1 = Label.objects.create(name ="plava", description = "for feature")
        l2 = Label.objects.create(name ="crvena", description = "for bug")
        l1.save()
        l2.save()
        # add collaborators
        collaborator1 = User.objects.create(id=3, username='collaborator1')
        repository.developers.add(collaborator1)
        collaborator2 = User.objects.create(id=4, username='collaborator2')
        repository.developers.add(collaborator2)
        repository.developers.add(user)
        # create milestone
        m1 = Milestone.objects.create(id = 1, title = 'Milestone1', description = 'first milestone', status = 'Opened', created=date.today(), due_date=date.today(), repository = repository)
        m2 = Milestone.objects.create(id = 2, title = 'Milestone2', description = 'second milestone', status = 'Opened', created=date.today(), due_date=date.today(), repository = repository)
        m1.save()
        m2.save()
        # create projects
        p1 = Project.objects.create(id = 1, name = 'project1', repository = repository)
        p2 = Project.objects.create(id = 2, name = 'project2', repository = repository)
        p1.save()
        p2.save()
        # create pullrequests
        pr1= Pullrequest.objects.create(id = 1, prRepository = repository)
        pr2 = Pullrequest.objects.create(id = 2, prRepository = repository)
        pr1.save()
        pr2.save()
        #create issue
        is1 = Iss.objects.create(id=11, issue_title='Issue1', milestone = m1,description=" issue for authors", state = "Opened", opened_by = user, repository=repository)
        is1.assignees.add(user)
        is1.projects.add(p1)
        is1.labels.add(l1)
        is1.labels.add(l2)
        is2 = Iss.objects.create(id=12, issue_title='Issue2', milestone = m2,description=" issue for projects", state = "Opened", opened_by = user, repository=repository)
        is2.assignees.add(user)
        is2.projects.add(p1)
        is2.labels.add(l1)
        is3 = Iss.objects.create(id=13, issue_title='task1', milestone = m2,description=" issue for labels", state = "Opened", opened_by = user2, repository=repository)
        is3.assignees.add(user)
        is3.projects.add(p2)
        is3.labels.add(l1)
        is4 = Iss.objects.create(id=14, issue_title='task2', milestone = m1,description=" issue for state", state = "Closed", opened_by = user, repository=repository)
        is4.assignees.add(user)
        is4.projects.add(p2)
        is4.labels.add(l2)
        

    def test_filter_by_title(self):
        is1 = Iss.objects.get(id = 11)
        is1 = Iss.objects.get(id = 12)
        is1 = Iss.objects.get(id = 13)
        is1 = Iss.objects.get(id = 14)
        repository = Repository.objects.get(id = 1)
        data = {}
        response = self.client.post(reverse('filter_issues', kwargs={'repo_id': repository.id, 'pk':"title:Issue1"}), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('issues' in response.context)
        self.assertEqual(len(response.context['issues']), 1)
    
    def test_filter_by_title_or_body(self):
        is1 = Iss.objects.get(id = 11)
        is1 = Iss.objects.get(id = 12)
        is1 = Iss.objects.get(id = 13)
        is1 = Iss.objects.get(id = 14)
        repository = Repository.objects.get(id = 1)
        data = {}
        response = self.client.post(reverse('filter_issues', kwargs={'repo_id': repository.id, 'pk':"issue"}), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('issues' in response.context)
        self.assertEqual(len(response.context['issues']), 4)
    
    def test_filter_by_project(self):
        is1 = Iss.objects.get(id = 11)
        is1 = Iss.objects.get(id = 12)
        is1 = Iss.objects.get(id = 13)
        is1 = Iss.objects.get(id = 14)
        repository = Repository.objects.get(id = 1)
        data = {}
        response = self.client.post(reverse('filter_issues', kwargs={'repo_id': repository.id, 'pk':"project:project1"}), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('issues' in response.context)
        self.assertEqual(len(response.context['issues']), 2)
    
    def test_filter_by_assigned(self):
        is1 = Iss.objects.get(id = 11)
        is1 = Iss.objects.get(id = 12)
        is1 = Iss.objects.get(id = 13)
        is1 = Iss.objects.get(id = 14)
        repository = Repository.objects.get(id = 1)
        data = {}
        response = self.client.post(reverse('filter_issues', kwargs={'repo_id': repository.id, 'pk':"assigned:testuser1"}), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('issues' in response.context)
        self.assertEqual(len(response.context['issues']), 4)

    def test_filter_by_label(self):
        is1 = Iss.objects.get(id = 11)
        is1 = Iss.objects.get(id = 12)
        is1 = Iss.objects.get(id = 13)
        is1 = Iss.objects.get(id = 14)
        repository = Repository.objects.get(id = 1)
        data = {}
        response = self.client.post(reverse('filter_issues', kwargs={'repo_id': repository.id, 'pk':"label:crvena"}), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('issues' in response.context)
        self.assertEqual(len(response.context['issues']), 2)



    def test_add_issue(self):
        client = Client()
        client.login(username='testuser1', password='testuser1')
        # get collaborators
        assignees = []
        assignees.append(User.objects.get(id=1).username)
        assignees.append(User.objects.get(id=2).username)
        # get projects
        projects_ids = []
        projects = Project.objects.all()
        for proj in projects:
            projects_ids.append(proj.id)
        # get pullrequeests
        pullrequests_ids = []
        pullrequests = Pullrequest.objects.all()
        # get milestone
        milestone_id = []
        milestone_id = Milestone.objects.all()
        for pr in pullrequests:
            pullrequests_ids.append(pr.id)
        data = {
            'title': 'Issue1', 
            'description':'first issue',
            'repository': 1,
            'milestone_id': milestone_id[0],
            'developers': assignees,
            'projects_ids': projects_ids,
            'pullrequests_ids': pullrequests_ids
            }
        response = client.post(reverse('add_issue'), data, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_view_issue(self):
        issue = Iss.objects.get(issue_title='Issue1')
        data = {}
        response = self.client.post(reverse('view_issue', kwargs={'id': issue.id}), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('milestones' in response.context)
        self.assertTrue('developers' in response.context)
        self.assertTrue('projects' in response.context)
        self.assertTrue('pullrequests' in response.context)
        self.assertEqual(len(response.context['milestones']), 2)
        self.assertEqual(len(response.context['developers']), 3)
        self.assertEqual(len(response.context['projects']), 2)
        self.assertEqual(len(response.context['pullrequests']), 2)
    
    def test_all_issues(self):
        data = {}
        response = self.client.post(reverse('all_issues'), data, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_all_issues_by_repository(self):
        data = {}
        response = self.client.post(reverse('issues', kwargs={'id': 1}), data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_update_issue(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='testuser', password='12345')
        issue = Iss.objects.get(id = 11)
        issue.issue_title = 'UpdatedTitle'
        issue.description = 'UpdatedDescription'
        # get collaborators
        assignees = []
        assignees.append(User.objects.get(id=1).username)
        # get projects
        projects_ids = []
        projects = Project.objects.all()
        for proj in projects:
            projects_ids.append(proj.id)
        # get pullrequeests
        pullrequests_ids = []
        pullrequests = Pullrequest.objects.all()
         # get milestone
        milestone_id = []
        milestone_id = Milestone.objects.all()
        for pr in pullrequests:
            pullrequests_ids.append(pr.id)
        data = {
            'title': issue.issue_title, 
            'description': issue.description,
            'state': 'Close',
            'milestone_id': milestone_id[0],
            'developers': assignees,
            'projects_ids': projects_ids,
            'pullrequests_ids': pullrequests_ids
            }
        response = client.post(reverse('update_issue', kwargs={'id': issue.id}),data, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_issue(self):
        issue = Iss.objects.get(id = 11)
        data = {}
        response = self.client.post(reverse('delete_issue', kwargs={'id': issue.id}),data, follow=True)
        self.assertEqual(response.status_code, 200)


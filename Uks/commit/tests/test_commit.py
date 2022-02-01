from django.test import TestCase
from repository.models import PRIVATE, Repository
from django.contrib.auth.models import User
from branch.models import Branch
from commit.models import Commit
from datetime import datetime



class CommitTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="user1", password="user1")
        repo = Repository.objects.create(name="repo", status=PRIVATE, creator=user)
        master = Branch.objects.create(name="master", is_default=True, repository=repo)
        develop = Branch.objects.create(name="develop", is_default=False, repository=repo)
        Commit.objects.create(message="First commit", date_time=datetime(2022,1,27), hash_id="ds7fgs4", branch=develop, author=user)

    def test_commit_message(self):
        commit = Commit.objects.get(message="First commit")
        self.assertEqual(commit.message, "First commit")

    
    def test_commit_hash_id(self):
        commit = Commit.objects.get(message="First commit")
        self.assertEqual(commit.hash_id, "ds7fgs4")

    def test_commit_branch(self):
        commit = Commit.objects.get(message="First commit")
        self.assertEqual(commit.branch.name, "develop")

    def test_commit_author(self):
        commit = Commit.objects.get(message="First commit")
        self.assertEqual(commit.author.username, "user1")



   









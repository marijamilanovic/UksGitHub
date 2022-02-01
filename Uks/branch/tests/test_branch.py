from django.test import TestCase, Client
from repository.models import PRIVATE, Repository
from django.contrib.auth.models import User
from branch.models import Branch

from django.urls import reverse, resolve

class BranchTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="user1", password="user1")
        repo = Repository.objects.create(name="repo", status=PRIVATE, creator=user)
        Branch.objects.create(name="master", is_default=True, repository=repo)
        Branch.objects.create(name="develop", is_default=False, repository=repo)

    def test_branch_is_default(self):
        master = Branch.objects.get(name="master")
        develop = Branch.objects.get(name="develop")
        self.assertEqual(master.is_default, True)
        self.assertEqual(develop.is_default, False)

    def test_branch_name(self):
        master = Branch.objects.get(name="master")
        develop = Branch.objects.get(name="develop")
        self.assertEqual(master.name, "master")
        self.assertEqual(develop.name, "develop")

    def test_branch_repo(self):
        master = Branch.objects.get(name="master")
        develop = Branch.objects.get(name="develop")
        self.assertEqual(master.repository.name, "repo")
        self.assertEqual(develop.repository.name, "repo")

  









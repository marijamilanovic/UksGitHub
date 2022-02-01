from django.test import TestCase
from milestone.models import Milestone
from django.contrib.auth.models import User
from pullrequest.models import Pullrequest
from pullrequest.views import try_merge
 
class PullrequestModelTest(TestCase):
    def setUp(self):
        pullrequest1 = Pullrequest.objects.create(name='master', status = 'Opened')
        reviewer = User.objects.create(username = 'user1')
        pullrequest1.reviewers.add(reviewer)
        pullrequest1 = Pullrequest.objects.create(name='develop', status = 'Opened', reviewed = True)



    def test_merge1(self):
        pullrequest = Pullrequest.objects.get(name='master')
        is_merged = try_merge(pullrequest)
        self.assertEquals(is_merged, False)

    def test_merge2(self):
        pullrequest = Pullrequest.objects.get(name='develop')
        is_merged = try_merge(pullrequest)
        self.assertEquals(is_merged, True)


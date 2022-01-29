from django.test import TestCase
from milestone.models import Milestone
 
class MilestoneModelTest(TestCase):
    def setUp(self):
        Milestone.objects.create(title='Milestone', description = 'aaaa', status = 'Opened')

    def test_title_label(self):
        milestone = Milestone.objects.get(title='Milestone')
        milestone_name = milestone._meta.get_field('title').verbose_name
        self.assertEquals(milestone_name, 'title')

    def test_description_label(self):
        milestone = Milestone.objects.get(title='Milestone')
        milestone_description = milestone._meta.get_field('description').verbose_name
        self.assertEquals(milestone_description, 'description')

    def test_status_label(self):
        milestone = Milestone.objects.get(title='Milestone')
        milestone_status = milestone._meta.get_field('status').verbose_name
        self.assertEquals(milestone_status, 'status')

    def test_title_max_length(self):
        milestone = Milestone.objects.get(title='Milestone')
        max_length = milestone._meta.get_field('title').max_length
        self.assertEquals(max_length, 50)

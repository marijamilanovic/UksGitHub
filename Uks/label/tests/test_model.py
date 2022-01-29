from django.test import TestCase
from label.models import Label

class LabelModelTest(TestCase):
    def setUp(self):
        Label.objects.create(name='Bug fix', description = 'bug fix label', color = '#af9bfa')

    def test_name_label(self):
        label = Label.objects.get(name='Bug fix')
        label_name = label._meta.get_field('name').verbose_name
        self.assertEquals(label_name, 'name')

    def test_description_label(self):
        label = Label.objects.get(name='Bug fix')
        label_description = label._meta.get_field('description').verbose_name
        self.assertEquals(label_description, 'description')

    def test_label_color_format(self):
        label = Label.objects.get(name='Bug fix')
        color_format = label._meta.get_field('color').format
        self.assertEquals(color_format, 'hexa')

    def test_name_max_length(self):
        label = Label.objects.get(name='Bug fix')
        max_length = label._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)
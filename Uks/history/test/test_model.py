from django.test import TestCase
from history.models import History
from django.contrib.auth.models import User

class HistoryModelTest(TestCase):
    def setUp(self):
        History.objects.create(message = 'message for history', changed_object_id = 1, object_type = 'Milestone')

    def test_message_history(self):
        history = History.objects.get(message = 'message for history')
        hystory_message = history._meta.get_field('message').verbose_name
        self.assertEquals(hystory_message, 'message')

    def test_object_type_pull_request(self):
        history = History.objects.get(message = 'message for history')
        history_object_type = history._meta.get_field('object_type').verbose_name
        self.assertEquals(history_object_type, 'object type')
from django.test import TestCase
from comment.models import Comment, Emoji
 
class CommentModelTest(TestCase):
    def setUp(self):
        Comment.objects.create(content='comment content')
    def test_content_label(self):
        comment = Comment.objects.get(content='comment content')
        comment_content = comment._meta.get_field('content').verbose_name
        self.assertEquals(comment_content, 'content')


class EmojiModelTest(TestCase):
    def setUp(self):
        Emoji.objects.create(name='127881')

    def test_name_label(self):
        emoji = Emoji.objects.get(name='127881')
        emoji_name= emoji._meta.get_field('name').verbose_name
        self.assertEquals(emoji_name, 'name')
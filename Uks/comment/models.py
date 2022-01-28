from pickle import EMPTY_SET
from unicodedata import name
from django.db import models
from enum import Enum

from django.contrib.auth.models import User

HEART = "129505"
ROCKET = "128640"
SAD = "128577"
HAPPY = "128512"
LIKE = "128077"
DISLIKE = "128077"
EYES = "128064"
PARTY = "127881"

EMOJI_PICKER = [
    (HEART, "129505"),
    (ROCKET, "128640"),
    (SAD, "128577"),
    (HAPPY, "128512"),
    (LIKE, "128077"),
    (DISLIKE, "128077"),
    (EYES, "128064"),
    (PARTY, "127881")
]


class Emoji(models.Model):
    name = models.CharField(max_length=20, choices=EMOJI_PICKER, default=HEART)
    reaction_creator =  models.ForeignKey(to=User, null=True, on_delete=models.CASCADE)


class Comment(models.Model):
    author = models.ForeignKey(to=User, null=True, on_delete=models.CASCADE)
    content = models.TextField(default='', blank= True)
    created_date = models.DateField(null=True, blank=True) 
    emojis = models.ManyToManyField(Emoji)

    def get_emoji_heart(self):
        return self.emojis.filter(name='129505').count()
    
    def get_emoji_rocket(self):
        return self.emojis.filter(name='128640').count()

    def get_emoji_sad(self):
        return self.emojis.filter(name='128577').count()
    
    def get_emoji_happy(self):
        return self.emojis.filter(name='128512').count()

    def get_emoji_like(self):
        return self.emojis.filter(name='128077').count()
    
    def get_emoji_dislike(self):
        return self.emojis.filter(name='128077').count()

    def get_emoji_eyes(self):
        return self.emojis.filter(name='128064').count()
    
    def get_emoji_party(self):
        return self.emojis.filter(name='127881').count()
    



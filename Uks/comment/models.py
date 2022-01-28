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
DISLIKE = "128078"
EYES = "128064"
PARTY = "127881"

EMOJI_PICKER = [
    (HEART, "129505"),
    (ROCKET, "128640"),
    (SAD, "128577"),
    (HAPPY, "128512"),
    (LIKE, "128077"),
    (DISLIKE, "128078"),
    (EYES, "128064"),
    (PARTY, "127881")
]


class Emoji(models.Model):
    name = models.CharField(max_length=20, choices=EMOJI_PICKER, default=HEART)
    reaction_creators =  models.ManyToManyField(User)


class Comment(models.Model):
    author = models.ForeignKey(to=User, null=True, on_delete=models.CASCADE)
    content = models.TextField(default='', blank= True)
    created_date = models.DateField(null=True, blank=True) 
    emojis = models.ManyToManyField(Emoji)

    def get_emoji_heart(self):
        emoji = self.emojis.filter(name='129505')
        return len(emoji[0].reaction_creators.all())
    
    def get_emoji_rocket(self):
        emoji = self.emojis.filter(name='128640')
        return len(emoji[0].reaction_creators.all())

    def get_emoji_sad(self):
        emoji = self.emojis.filter(name='128577')
        return len(emoji[0].reaction_creators.all())
    
    def get_emoji_happy(self):
        emoji =  self.emojis.filter(name='128512')
        return len(emoji[0].reaction_creators.all())

    def get_emoji_like(self):
        emoji =  self.emojis.filter(name='128077')
        return len(emoji[0].reaction_creators.all())
    
    def get_emoji_dislike(self):
        emoji =  self.emojis.filter(name='128078')
        return len(emoji[0].reaction_creators.all())

    def get_emoji_eyes(self):
        emoji =  self.emojis.filter(name='128064')
        return len(emoji[0].reaction_creators.all())
    
    def get_emoji_party(self):
        emoji =  self.emojis.filter(name='127881')
        return len(emoji[0].reaction_creators.all())
    



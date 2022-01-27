from pickle import EMPTY_SET
from django.db import models
from enum import Enum

from django.contrib.auth.models import User

HEART = "129505"
ROCKET = "128640"
SAD = "128577"
HAPPY = "128512"
LIKE = "128077"
DISLIKE = "128077"
EMOJI_PICKER = [
    (HEART, "129505"),
    (ROCKET, "128640"),
    (SAD, "128577"),
    (HAPPY, "128512"),
    (LIKE, "128077"),
    (DISLIKE, "128077")
]


class Emoji(models.Model):
    name = models.CharField(max_length=20, choices=EMOJI_PICKER, default=HEART)
    reaction_creator =  models.ForeignKey(to=User, null=True, on_delete=models.CASCADE)


class Comment(models.Model):
    author = models.ForeignKey(to=User, null=True, on_delete=models.CASCADE)
    content = models.TextField(default='', blank= True)
    created_date = models.DateField(null=True, blank=True) 
    emojis = models.ManyToManyField(Emoji)



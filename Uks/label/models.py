from django.db import models

class Label(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='', blank= True)
    #color = ColorField(format='hexa')

    def __str__(self):
        return self.name
from __future__ import unicode_literals

from django.db import models
from inventory.models import Beer

# Create your models here.
class Rate(models.Model):
    rating = models.SmallIntegerField() # this will be modded by 100
    beer = models.ForeignKey(Beer)
    def __str__(self):
        if self.rating and self.beer:
            return "{0}: {1}".format(str(self.beer),self.rating)
        return self

class Raters(models.Model):
    rate = models.ForeignKey(Rate)
    ip = models.CharField(unique=True, max_length=128)

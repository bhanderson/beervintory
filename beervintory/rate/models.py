from __future__ import unicode_literals

from django.db import models
from inventory.models import Beer

# Create your models here.
class Rate(models.Model):
    rating = models.SmallIntegerField() # this will be modded by 100
    beer = models.ForeignKey(Beer)


from __future__ import unicode_literals

from django.db import models
from inventory.models import Beer

# Create your models here.
class Rate(models.Model):
    rating = models.SmallIntegerField()#editable=False) # this will be modded by 100
    #beer = models.ForeignKey(Beer, unique=True)
    beer = models.OneToOneField(Beer)
    raters = models.TextField()#editable=False) # json dict of ip : rating
    def __str__(self):
        return "{0}: {1}".format(str(self.beer), str(self.rating))
        return self
        return "error"

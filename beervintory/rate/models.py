from __future__ import unicode_literals

from django.db import models
from inventory.models import Beer
import json

# Create your models here.
class Rate(models.Model):
    rating = models.SmallIntegerField(editable=False) # this will be modded by 100
    beer = models.OneToOneField(Beer, editable=False)
    raters = models.TextField(editable=False) # json dict of ip : rating
    def __str__(self):
        jd = json.decoder.JSONDecoder()
        d = jd.decode(self.raters)
        return "{0}: {1} - {2} rater(s)".format(str(self.rating),
                                                str(self.beer), len(d))
        return self
        return "error"

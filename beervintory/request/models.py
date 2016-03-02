from __future__ import unicode_literals

from django.db import models
from inventory import models as inv

# Create your models here.
class Request(models.Model):
    number = models.SmallIntegerField(default = 0)
    #beer = models.ForeignKey(inv.Beer, null=True, unique=True)
    #beer = models.OneToOneField(inv.Beer, primary_key=True)
    beer = models.CharField(max_length=30, null=True)
    def __str__(self):
            return "{0} ||  {1} request(s)".format(self.beer, self.number)

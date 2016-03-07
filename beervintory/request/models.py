from __future__ import unicode_literals

from django.db import models
from inventory import models as inv

# Create your models here.
class Request(models.Model):
    number = models.SmallIntegerField(default = 0)#, editable=False)
    beer = models.CharField(unique=True,max_length=30)
    requesters = models.TextField()#editable=False)
    def __str__(self):
        return "{0} ||  {1} request(s)".format(self.beer, self.number)

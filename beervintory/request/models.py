from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Request(models.Model):
    style = models.CharField(max_length=50, unique=True, default="Style")
    brewer = models.CharField(max_length=50, unique=True, default="Brewer")

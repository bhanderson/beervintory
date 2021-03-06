from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.
class Floor(models.Model):
    number = models.SmallIntegerField(unique=True)
    def __str__(self):
        if self.number:
            s = ['st','nd','rd','th']
            suffix = s[0]
            if self.number > 3:
                suffix = s[3]
            else:
                suffix = s[self.number-1]
            return "{0}{1}".format(self.number, suffix)
        return self

class Kegerator(models.Model):
    co2_date = models.DateField(default=timezone.now)
    clean_date = models.DateField(default=timezone.now)
    floor = models.ForeignKey(Floor, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="Kegerator", unique=True)
    def _to_dict(self):
        info = {
                'co2_date': str(self.co2_date),
                'clean_date': str(self.clean_date),
                'floor': str(self.floor),
                'name': str(self.name)
                }
        return info
    def __str__(self):
        if self.name:
            return str(self.name)
        else:
            return self

class Style(models.Model):
    name = models.CharField(max_length=50, unique=True, default="Style")
    def __str__(self):
        if self.name:
            return self.name
        return self

class Brewer(models.Model):
    name = models.CharField(max_length=50, unique=True, default="Brewer")
    def __str__(self):
        if self.name:
            return self.name
        return self

class Beer(models.Model):
    abv = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    ba_score = models.SmallIntegerField()
    link = models.CharField(max_length=100, default="Link to Beer")
    brewer = models.ForeignKey(Brewer, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="Name", unique=True)
    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    def _to_dict(self):
        info = {
                'name': str(self.name),
                'style': str(self.style),
                'brewer': str(self.brewer),
                'abv': str(self.abv),
                'ba_score': str(self.ba_score),
                'link': str(self.link)
                }
        return info
    def __str__(self):
        if self.name or self.style or self.brewer:
            return "{0} {1} | {2}".format(self.name, self.style, self.brewer)
        return self
    class Meta:
        ordering = ["name"]

class Keg(models.Model):
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)
    kegerator = models.ForeignKey(Kegerator, blank=True, null=True, on_delete=models.CASCADE)
    chilled = models.BooleanField(default=False)
    filled = models.BooleanField(default=False)
    stocked = models.BooleanField(default=False)
    tapped = models.BooleanField(default=False)
    chilled_date = models.DateField(default=timezone.now)
    emptied_date = models.DateField(default=timezone.now)
    stocked_date = models.DateField(default=timezone.now)
    tapped_date = models.DateField(default=timezone.now)
    def _to_dict(self):
        info = {
                'beer': self.beer._to_dict() if self.beer else None,
                'kegerator': self.kegerator._to_dict() if self.kegerator else None,
                'chilled': str(self.chilled),
                'filled': str(self.filled),
                'stocked': str(self.stocked),
                'tapped': str(self.tapped),
                'chilled_date': str(self.chilled_date),
                'emptied_date': str(self.emptied_date),
                'stocked_date': str(self.stocked_date),
                'tapped_date': str(self.tapped_date)
                }
        return info
    def __str__(self):
        cold = "Warm"
        full = "Empty"
        if self.beer:
            if self.chilled:
                cold = "Cold"
            if self.filled:
                full = "Full"
            return '{0} {1} | {2}, {3}'.format(self.beer.name, self.beer.style, full,
                cold)
        else:
            return 'None | {0}, {1}'.format(full,cold)
        return self
    class Meta:
        ordering = ["beer"]

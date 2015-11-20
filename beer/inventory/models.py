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
    floor = models.ForeignKey(Floor, blank=True, null=True)
    name = models.CharField(max_length=50, default="Name", unique=True)
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
    isi_score = models.SmallIntegerField()
    link = models.CharField(max_length=100, default="Link to Beer")
    brewer = models.ForeignKey(Brewer)
    name = models.CharField(max_length=50, default="Name", unique=True)
    style = models.ForeignKey(Style)
    def __str__(self):
        if self.name or self.style or self.brewer:
            return "{0} {1} | {2}".format(self.name, self.style, self.brewer)
        return self

class Keg(models.Model):
    beer = models.ForeignKey(Beer)
    kegerator = models.ForeignKey(Kegerator)
    chilled = models.BooleanField(default=False)
    filled = models.BooleanField(default=False)
    stocked = models.BooleanField(default=False)
    tapped = models.BooleanField(default=False)
    chilled_date = models.DateField(default=timezone.now)
    emptied_date = models.DateField(default=timezone.now)
    stocked_date = models.DateField(default=timezone.now)
    tapped_date = models.DateField(default=timezone.now)
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

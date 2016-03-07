from django import forms
from inventory import models

class BeerForm(forms.Form):
    beer = forms.ModelChoiceField(models.Beer.objects.all())

class RateForm(forms.Form):
    rating = forms.IntegerField(label="Rating out of 100")

from django import forms
from inventory import models
import models

class RequestForm(forms.Form):
    request = forms.ModelChoiceField(models.Request.objects.all())

class NewRequestForm(forms.Form):
    new_request = forms.CharField(label="New Request", max_length=50)

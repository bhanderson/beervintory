from django import forms
from .models import Request

class RequestForm(forms.Form):
    request = forms.ModelChoiceField(Request.objects.all())

class NewRequestForm(forms.Form):
    new_request = forms.CharField(label="New Request", max_length=50)

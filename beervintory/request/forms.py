from django import forms
from inventory import models
import models

class RequestForm(forms.Form):
    request = forms.ModelChoiceField(models.Request.objects.all(),
    empty_label='----New----', )


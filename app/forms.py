from flask.ext.wtf import Form
from wtforms import (TextField, DecimalField, IntegerField, SelectField,
SubmitField, DateField, BooleanField)
from wtforms.fields import FormField
from wtforms.validators import DataRequired
from . import models

from wtforms_alchemy import ModelForm, ModelFieldList

class BeerForm(Form):
    abv = DecimalField('abv', places=2)
    ba_score = IntegerField('ba')
    brewer = TextField('brewer')
    isi_score = IntegerField('isi')
    link = TextField('link')
    name = TextField('name')
    style = TextField('style')

class KegForm(Form):
    #beer = ModelFieldList(FormField(BeerForm))
    beers =models.Beer.query.all()
    l = []
    for beer in beers:
        l.append((beer, beer.__repr__()))
    beer = SelectField(coerce=models.Beer, choices = l)
    chilled = BooleanField()
    filled = BooleanField()
    tapped = BooleanField()
    submit = SubmitField()

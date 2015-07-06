from flask.ext.wtf import Form
from wtforms import (TextField, DecimalField, IntegerField, SelectField,
SubmitField, DateField, BooleanField, SelectMultipleField)
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
        l.append((beer.id, beer.__repr__()))
    beer = SelectField(coerce=int, choices = l)
    chilled = BooleanField()
    filled = BooleanField()
    tapped = BooleanField()
    submit = SubmitField()

class KegeratorForm(Form):
    kegs = models.Keg.query.all()
    l = []
    for keg in kegs:
        l.append((keg.id, keg.__repr__()))
    co2 = BooleanField()
    floor = SelectField(coerce=int, choices = l)
    name = TextField('name')
    submit = SubmitField()

class FloorForm(Form):
    number = IntegerField()
    kegerators = models.Kegerator.query.all()
    l = []
    for kegerator in kegerators:
        l.append((kegerator.id, kegerator.__repr__()))
    kegerators = SelectMultipleField(choices=l, coerce=int)
    submit = SubmitField()


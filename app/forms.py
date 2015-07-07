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
    submit = SubmitField()

class KegForm(Form):
    beers = models.Beer.query.all()
    options = [(b.id, b.__repr__()) for b in beers]
    beer = SelectField(coerce=int, choices=options)
    chilled = BooleanField()
    filled = BooleanField()
    tapped = BooleanField()
    submit = SubmitField()

class KegeratorForm(Form):
    kegs = models.Keg.query.all()
    koptions = [(k.id, k.__repr__()) for k in kegs]
    keg = SelectField(coerce=int, choices=koptions)
    floors = models.Floor.query.all()
    foptions = [(f.id, f.__repr__()) for f in floors]
    floor = SelectField(coerce=int, choices=foptions)
    co2 = BooleanField()
    name = TextField('Name')
    submit = SubmitField()

class FloorForm(Form):
    kegerators = models.Kegerator.query.all()
    options = [(k.id, k.__repr__()) for k in kegerators]
    kegerators = SelectMultipleField(coerce=int, choices=options)
    number = IntegerField()
    submit = SubmitField()


from flask.ext.wtf import Form
from wtforms import (TextField, DecimalField, IntegerField, SelectField,
SubmitField, DateField, BooleanField, SelectMultipleField)
from wtforms.fields import FormField
from wtforms.validators import DataRequired
from . import models

from wtforms_alchemy import ModelForm, ModelFieldList

class BeerForm(Form):
    '''Form for beer.
    Information about the beer'''
    abv = DecimalField('abv', places=2)
    ba_score = IntegerField('ba')
    brewer = TextField('brewer')
    isi_score = IntegerField('isi')
    link = TextField('link')
    name = TextField('name')
    style = TextField('style')
    submit = SubmitField()

class KegForm(Form):
    '''Form for a keg containing beer.
    Each keg has a beer and information about the keg.'''
    beer = SelectField(coerce = int)
    chilled = BooleanField()
    filled = BooleanField()
    tapped = BooleanField()
    stocked = BooleanField('stocked')
    submit = SubmitField()

class KegeratorForm(Form):
    '''Form for each Kegerator containing a keg.
    Each kegerator is on a floor and has a keg'''
    floor = SelectField(coerce = int)
    keg = SelectField(coerce = int)
    co2 = BooleanField()
    name = TextField('Name')
    submit = SubmitField()

class FloorForm(Form):
    '''Form for each floor containing kegerators.
    A floor can have many kegerators'''
    kegerators = SelectMultipleField()
    number = IntegerField()
    submit = SubmitField()


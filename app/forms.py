from flask.ext.wtf import Form
from wtforms import (TextField, DecimalField, IntegerField, SelectField,
SubmitField, DateField, BooleanField, SelectMultipleField)
from wtforms.fields import FormField
from wtforms.validators import DataRequired, Optional
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
    beer_id = SelectField(coerce = int, validators=[DataRequired()])
    kegerator_id = SelectField(coerce = int, validators=[DataRequired()])
    chilled = BooleanField()
    chilled_date = DateField()
    empty_date = DateField()
    filled = IntegerField('filled')
    stocked = BooleanField('stocked')
    stocked_date = DateField()
    submit = SubmitField()
    tapped = BooleanField()
    tapped_date = DateField()

class KegeratorForm(Form):
    '''Form for each Kegerator containing a keg.
    Each kegerator is on a floor and has a keg'''
    clean_date = DateField()
    co2 = BooleanField()
    co2_date = DateField()
    floor_id = SelectField(coerce = int)
    kegs = SelectMultipleField(coerce = int, validators=[Optional()])
    name = TextField('Name')
    submit = SubmitField()

class FloorForm(Form):
    '''Form for each floor containing kegerators.
    A floor can have many kegerators'''
    kegerators = SelectMultipleField()
    number = IntegerField()
    submit = SubmitField()

class VoteForm(Form):
    """Form for making a new vote."""
    beer = SelectMultipleField()
    rating = IntegerField()
    submit = SubmitField()

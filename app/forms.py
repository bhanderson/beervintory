from flask.ext.wtf import Form
from wtforms import (TextField, DecimalField, IntegerField, SelectField,
SubmitField, DateField, BooleanField, SelectMultipleField)
from wtforms.fields import FormField
from wtforms.validators import DataRequired, Optional
from . import models

from wtforms_alchemy import ModelForm, ModelFieldList

class FloorForm(Form):
    '''Form for each floor containing kegerators.
    A floor can have many kegerators'''
    kegerators = SelectMultipleField(validators=[Optional()])
    number = IntegerField()
    submit = SubmitField()

class KegeratorForm(Form):
    '''Form for each Kegerator containing a keg.
    Each kegerator is on a floor and has a keg'''
    clean_date = DateField()
    co2 = BooleanField()
    co2_date = DateField()
    floor_id = SelectField(coerce = int, validators=[Optional()])
    kegs = SelectMultipleField(coerce = int, validators=[Optional()])
    name = TextField('Name')
    submit = SubmitField()

class KegForm(Form):
    '''Form for a keg containing beer.
    Each keg has a beer and information about the keg.'''
    beer_id = SelectField('Beer', coerce = int, validators=[DataRequired()])
    chilled = BooleanField()
    chilled_date = DateField(validators=[Optional()])
    empty_date = DateField(validators=[Optional()])
    filled = IntegerField('filled')
    kegerator_id = SelectField(coerce = int, validators=[Optional()])
    stocked = BooleanField('stocked')
    stocked_date = DateField()
    submit = SubmitField()
    tapped = BooleanField()
    tapped_date = DateField(validators=[Optional()])

class BeerForm(Form):
    '''Form for beer.
    Information about the beer'''
    abv = DecimalField('abv', places=2)
    ba_score = IntegerField('ba', validators=[Optional()])
    brewer = TextField('brewer')
    isi_score = IntegerField('isi', validators=[Optional()])
    kegs = SelectMultipleField(coerce = int, validators=[Optional()])
    link = TextField('link')
    name = TextField('name')
    style = TextField('style')
    submit = SubmitField()

class VoteForm(Form):
    """Form for making a new vote."""
    beer = SelectField()
    rating = IntegerField()
    submit = SubmitField()

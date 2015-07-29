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
    kegerators = SelectMultipleField('Kegerators', validators=[Optional()])
    number = IntegerField('Floor Number')
    submit = SubmitField()

class KegeratorForm(Form):
    '''Form for each Kegerator containing a keg.
    Each kegerator is on a floor and has a keg'''
    clean_date = DateField('Clean Date (YYYY-MM-DD)')
    co2 = BooleanField('CO2')
    co2_date = DateField('CO2 Date')
    floor_id = SelectField('Floor', coerce=int, validators=[Optional()])
    kegs = SelectMultipleField('Kegs', coerce = int, validators=[Optional()])
    name = TextField('Name')
    submit = SubmitField()

class KegForm(Form):
    '''Form for a keg containing beer.
    Each keg has a beer and information about the keg.'''
    beer_id = SelectField('Beer', coerce=int, validators=[DataRequired()])
    chilled = BooleanField('Chilled')
    chilled_date = DateField('Chilled Date (YYYY-MM-DD)', validators=[Optional()])
    empty_date = DateField('Empty Date (YYYY-MM-DD)', validators=[Optional()])
    filled = IntegerField('Filled')
    kegerator_id = SelectField('Kegerator', coerce=int, validators=[Optional()])
    stocked = BooleanField('Stocked')
    stocked_date = DateField('Stocked Date (YYYY-MM-DD)')
    submit = SubmitField()
    tapped = BooleanField('Tapped')
    tapped_date = DateField('Tapped Date (YYYY-MM-DD)', validators=[Optional()])

class BeerForm(Form):
    '''Form for beer.
    Information about the beer'''
    abv = DecimalField('ABV:', places=2)
    ba_score = IntegerField('Beer Advocate Score:', validators=[Optional()])
    brewer = TextField('Brewer')
    isi_score = IntegerField('Isilon Score', validators=[Optional()])
    kegs = SelectMultipleField('Kegerators', coerce = int, validators=[Optional()])
    link = TextField('Beer Advocate Link')
    name = TextField('Name')
    style = TextField('Style')
    submit = SubmitField()

class VoteForm(Form):
    """Form for making a new vote."""
    beer_id = SelectField('Beer', coerce=int)
    rating = IntegerField()
    submit = SubmitField()

class RequestForm(Form):
    """Form for making a request"""
    beer_name = TextField('Beer Name')
    submit = SubmitField()

from flask.ext.wtf import Form
from wtforms import TextField, DecimalField, IntegerField
from wtforms.fields import FormField
from wtforms.validators import DataRequired

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
    beer = ModelFieldList(FormField(BeerForm))

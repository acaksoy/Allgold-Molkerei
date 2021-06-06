from flask_wtf import Form
from wtforms import StringField, IntegerField,validators

class verkaufStelleForm(Form):
    name = StringField('name', [validators.DataRequired()])
    typ = StringField('name', [validators.DataRequired()])
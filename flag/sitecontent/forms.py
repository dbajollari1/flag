from wtforms import Form, StringField, TextAreaField, DateField, BooleanField, SelectField, HiddenField, SubmitField, validators, ValidationError
import datetime

class SiteContentForm(Form):
    siteContentTitle = StringField('Title', [validators.Length(min=0, max=100)])
    siteContentDesc = TextAreaField('Content', [validators.Length(min=1, max=2000), validators.DataRequired()])
    siteContentId = HiddenField()

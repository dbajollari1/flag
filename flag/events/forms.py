from wtforms import Form, StringField, TextAreaField, DateField, BooleanField, SubmitField, validators, ValidationError
import datetime

class EventForm(Form):
    eventTitle = StringField('Title', [validators.Length(min=4, max=100), validators.DataRequired()])
    eventDate = DateField('Event Date', [validators.DataRequired('Please enter event date in mm/dd/yyyy format')], format='%m/%d/%Y', default=datetime.date.today())
    eventLocation = TextAreaField('Location', [validators.Length(min=1, max=100), validators.DataRequired()])
    eventDesc = TextAreaField('Description', [validators.Length(min=1, max=500), validators.DataRequired()])


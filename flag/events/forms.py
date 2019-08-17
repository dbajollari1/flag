from wtforms import Form, StringField, TextAreaField, DateField, BooleanField, SelectField, HiddenField, SubmitField, validators, ValidationError
import datetime

class EventForm(Form):
    eventTitle = StringField('Title', [validators.Length(min=4, max=100), validators.DataRequired()])
    eventDate = DateField('Event Date', [validators.DataRequired('Please enter event date in mm/dd/yyyy format')], format='%m/%d/%Y', default=datetime.datetime.today().strftime('%m/%d/%Y'))
    eventLocation = TextAreaField('Location', [validators.Length(min=1, max=100), validators.DataRequired()])
    eventDesc = TextAreaField('Details', [validators.Length(min=1, max=1000), validators.DataRequired()])
    startTime = SelectField('From')
    endTime = SelectField('To')
    eventID = HiddenField()

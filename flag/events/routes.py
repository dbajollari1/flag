from flask import render_template, redirect, url_for, request, flash, redirect
from flag.events import bpEvents
from flag.events.models import Event
from flag.dataaccess.eventsDAO import getEvents, saveEvent, getEvent, updateEvent, deleteEvent
from flag.events.forms import EventForm
import datetime
from flask_login import login_required, current_user
from flask import current_app as app

@bpEvents.route('/events')
def events():
    try:
        eventList= getEvents()
        return render_template('events/events.html', eventList = eventList)
    except Exception as e:
        app.logger.error(str(e), extra={'user': ''})
        return redirect(url_for('errors.error'))

@bpEvents.route('/event/<event_id>', methods=('GET', 'POST'))
@login_required
def event(event_id = 0):
    if current_user.userRole != 'A':
        app.logger.error('Unauthorized!!!!', extra={'user': current_user.email})
        return redirect(url_for('errors.error'))
    
    form = EventForm(request.form)

    fromchoices=[]
    for x in range(6,12):
        fromchoices.append((str(x) + ":00 AM", str(x) + ":00 AM"))
        fromchoices.append((str(x) + ":30 AM", str(x) + ":30 AM"))      
    fromchoices.append(( "12:00 PM", "12:00 PM"))
    fromchoices.append(("12:30 PM", "12:30 PM"))
    for x in range(1,12):
        fromchoices.append((str(x) + ":00 PM", str(x) + ":00 PM"))
        fromchoices.append(( str(x) + ":30 PM", str(x) + ":30 PM"))
    form.startTime.choices = fromchoices
    form.endTime.choices = fromchoices

    if request.method == "GET":
        form.eventID.data = event_id
        if int(form.eventID.data) > 0:
            event = getEvent(event_id)
            form.eventTitle.data = event.eventTitle
            form.eventDate.data = event.eventDate
            form.eventLocation.data = event.eventLocation
            form.eventDesc.data = event.eventDesc
            form.startTime.data = event.startTime
            form.endTime.data = event.endTime
        else:
            form.startTime.data="7:00 PM"
            form.endTime.data="9:00 PM"
            form.eventDate.data = datetime.datetime.today().strftime('%m/%d/%Y')

    if request.method == "POST":
        if form.validate() == False:
            try:
                form.eventDate.data = form.eventDate.data.strftime('%m/%d/%Y')
            except:
                pass
            return render_template('events/event.html',form = form) 
        #save to db
        try:
            event = Event(form.eventID.data, form.eventTitle.data, form.eventLocation.data, form.eventDesc.data, form.eventDate.data, form.startTime.data, form.endTime.data)
            if int(form.eventID.data) > 0:
                updateEvent(event)
            else:
                saveEvent(event)
            return redirect("/events") #go to events page
        except Exception as e:
            app.logger.error(str(e), extra={'user': ''})
            return redirect(url_for('errors.error'))

    return render_template('events/event.html',form = form)

@bpEvents.route('/removeEvent/<event_id>')
@login_required
def removeEvent(event_id = 0):
    try: 
        if current_user.userRole != 'A':
            app.logger.error('Unauthorized!!!!', extra={'user': current_user.email})
            return redirect(url_for('errors.error'))
        deleteEvent(event_id)
        return redirect("/events") #reload page
    except Exception as e:
        app.logger.error(str(e), extra={'user': ''})
        return redirect(url_for('errors.error'))

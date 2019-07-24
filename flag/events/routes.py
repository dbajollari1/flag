from flask import render_template, redirect, url_for, request, flash, redirect
from flag.events import bpEvents
from flag.events.models import Event
from flag.dataaccess.events import getEvents, saveEvent
from flag.events.forms import EventForm
import datetime

@bpEvents.route('/events')
def events():
    eventList= getEvents()
    return render_template('events/events.html', eventList = eventList)


@bpEvents.route('/event', methods=('GET', 'POST'))
def event():
    form = EventForm(request.form)
    print('before post')
    if request.method == "POST":
        if form.validate() == False:    
            return render_template('events/event.html',form = form) 
        #save to db
        try:
            event = Event(form.eventTitle.data, form.eventDate.data, form.eventLocation.data, form.eventDesc.data)    
            saveEvent(event)
            return redirect("/events") #go to events page
        except:
            print('failed.....')

    return render_template('events/event.html',form = form)


from flag.dataaccess.db_helper import execute_sql
from flag.events.models import Event
import datetime

def getEvents():
    eventList=[]
    events = execute_sql(
        'SELECT event.id, event.title, event.description, event.location, event.eventdate FROM event')

    for row in events:
        event = Event()
        event.eventTitle = row['title']
        event.eventDesc = row['description']
        event.eventLocation = row['location']
        event.eventDate = row['eventdate']
        eventList.append(event)

    return eventList

def saveEvent(event): 
    sql = 'INSERT into event (title, description, location, eventDate, status, createdBy, createdOn) VALUES (?, ?, ?, ?, ?, ?, ?)'
    execute_sql (sql, (event.eventTitle, event.eventDesc, event.eventLocation, 
    event.eventDate, 'A', 'David',datetime.datetime.now()), True)
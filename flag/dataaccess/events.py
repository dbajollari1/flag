from flag.dataaccess.db_helper import execute_sql
from flag.events.models import Event
import datetime

def getEvents():
    eventList=[]
    events = execute_sql(
        "SELECT event.id, event.title, event.description, event.location, event.eventDate, event.startTime, event.endTime FROM event WHERE event.eventDate >= date('now') ORDER BY event.eventDate")

    for row in events:
        event = Event()
        event.eventId = row['id']
        event.eventTitle = row['title']
        event.eventDesc = row['description'].split('\n') #.replace("\n", "<br/>")
        event.eventLocation = row['location']
        event.eventDate = datetime.datetime.strptime(row['eventdate'],'%Y-%m-%d').strftime('%d-%b-%Y')
        event.startTime = row['startTime']
        event.endTime = row['endTime']
        eventList.append(event)
        
    return eventList


def getEvent(event_id):
    sql = 'SELECT * from event where id = ?'
    row = execute_sql (sql, (event_id,), False, True)
    event = Event()
    event.eventTitle = row['title']
    event.eventDesc = row['description']
    event.eventLocation = row['location']
    event.eventDate = datetime.datetime.strptime(row['eventdate'],'%Y-%m-%d').strftime('%m/%d/%Y')
    event.startTime = row['startTime']
    event.endTime = row['endTime']
    return event

def saveEvent(event): 
    sql = 'INSERT into event (title, description, location, eventDate, startTime, endTime, status, createdBy, createdOn) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
    execute_sql (sql, (event.eventTitle, event.eventDesc, event.eventLocation, 
    event.eventDate, event.startTime, event.endTime, 'A', 'David',datetime.datetime.now()), True)

def deleteEvent(event_id):
    sql = 'DELETE from event where id = ?'
    execute_sql (sql, (event_id,), True, False)

def updateEvent(event):
    sql = 'UPDATE event set title = ? , description = ?, location = ? , eventDate = ?, startTime = ?, endTime = ?, status = ? , createdBy = ?, createdOn = ? WHERE id = ?'
    execute_sql(sql, (event.eventTitle, event.eventDesc, event.eventLocation, 
    event.eventDate, event.startTime, event.endTime, 'A', 'David',datetime.datetime.now(), event.eventId),  True)

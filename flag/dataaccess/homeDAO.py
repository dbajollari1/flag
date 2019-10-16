from flag.dataaccess.db_helper import execute_sql
from flag.events.models import Event
from flag.sitecontent.models import SiteContent
import datetime

def getUpcomingEvent():
    sql = "SELECT * from event where eventDate >= date('now') Order by eventDate LIMIT 1"
    row = execute_sql (sql,(), False, True)
    if not row == None:
        event = Event()
        event.eventTitle = row['title']
        event.eventDesc = row['description']
        event.eventLocation = row['location']
        event.eventDate = datetime.datetime.strptime(row['eventdate'],'%Y-%m-%d').strftime('%m/%d/%Y')
        event.startTime = row['startTime']
        event.endTime = row['endTime']
        return event

def getSiteContents():
    siteContentList=[]
    siteContents = execute_sql(
        "SELECT sitecontent.id, sitecontent.title, sitecontent.description, sitecontent.isHtml From sitecontent")

    for row in siteContents:
        siteContent = SiteContent()
        siteContent.siteContentId = row['id']
        siteContent.siteContentTitle = row['title']
        siteContent.isHtml = row['isHtml']
        if siteContent.isHtml == 'Y':
            siteContent.siteContentDesc = row['description']
        else:
            siteContent.siteContentDesc = row['description'].split('\n') #.replace("\n", "<br/>")
        siteContentList.append(siteContent)
        
    return siteContentList
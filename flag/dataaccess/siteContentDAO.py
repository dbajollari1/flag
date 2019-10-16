from flag.dataaccess.db_helper import execute_sql
from flag.sitecontent.models import SiteContent
import datetime

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


def getSiteContent(siteContent_id):
    sql = 'SELECT * from sitecontent where id = ?'
    row = execute_sql (sql, (siteContent_id,), False, True)
    siteContent = SiteContent()
    siteContent.siteContentTitle = row['title']
    siteContent.siteContentDesc = row['description']
    siteContent.isHtml = row['isHtml']
    return siteContent

def saveSiteContent(siteContent): 
    sql = 'INSERT into sitecontent (title, description, isHtml, createdBy, createdOn) VALUES (?, ?, ?, ?, ?)'
    execute_sql (sql, (siteContent.siteContentTitle, siteContent.siteContentDesc, siteContent.isHtml, 'David',datetime.datetime.utcnow()), True)

def deleteSiteContent(siteContent_id):
    sql = 'DELETE from sitecontent where id = ?'
    execute_sql (sql, (siteContent_id,), True, False)

def updateSiteContent(siteContent):
    sql = 'UPDATE sitecontent set title = ? , description = ?, isHtml = ?, createdBy = ?, createdOn = ? WHERE id = ?'
    execute_sql(sql, (siteContent.siteContentTitle, siteContent.siteContentDesc, siteContent.isHtml, 'David',datetime.datetime.utcnow(), siteContent.siteContentId),  True)


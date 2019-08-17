from flag.dataaccess.db_helper import execute_sql
from flag.gallery.models import Photo
import datetime
# from base64 import b64encode
# import sqlite3 as lite

def getPhotos(filter = 'A', userId = ''):
    photoList = []
    photos = None
    if filter == 'U': #photos uploaded by a specific user
        photos = execute_sql('SELECT gallery.photoId, gallery.photoTitle, gallery.photoFileName, gallery.uploadDate, gallery.uploadBy FROM gallery Where gallery.uploadBy = ? Order By uploadDate desc', (userId,))
    else: #all photos
        photos = execute_sql('SELECT gallery.photoId, gallery.photoTitle, gallery.photoFileName, gallery.uploadDate, gallery.uploadBy FROM gallery Order By uploadDate desc')

    for row in photos:
        photo = Photo()
        photo.photoId = row['photoId']
        photo.photoTitle = row['photoTitle']
        photo.photoFileName = row['photoFileName']
        photo.uploadDate = row['uploadDate']
        photo.uploadBy = row['uploadBy']
        #photo.photoImg = b64encode(row['photo']).decode("utf-8")

        photoList.append(photo)

    return photoList


def savePhoto(photo):
    sql = 'INSERT into gallery (photoTitle, photoFileName, uploadDate, uploadBy) VALUES ( ?, ?, ?, ?)' #, photo
    execute_sql(sql, (photo.photoTitle, photo.photoFileName, datetime.datetime.now(), photo.uploadBy), True) #, lite.Binary(photo.photoImg)

def deletePhoto(photoId):
    sql = 'DELETE FROM gallery WHERE photoId = ?'
    execute_sql(sql, (photoId,), True)


def getPhoto(photoId):
    sql = 'SELECT gallery.photoId, gallery.photoTitle, gallery.photoFileName, gallery.uploadDate, gallery.uploadBy FROM gallery WHERE photoId = ?'
    row = execute_sql(sql, (photoId,), False, True)

    photo = Photo()
    photo.photoId = row['photoId']
    photo.photoTitle = row['photoTitle']
    photo.photoFileName = row['photoFileName']
    photo.uploadDate = row['uploadDate']
    photo.uploadBy = row['uploadBy']

    return photo
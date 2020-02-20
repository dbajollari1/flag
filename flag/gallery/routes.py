from flask import render_template, redirect, url_for, request, flash, redirect
from flag.gallery import bpGallery
from flask import current_app as app
import os, datetime
from werkzeug.utils import secure_filename
from flag.dataaccess.galleryDAO import getPhotos, savePhoto, deletePhoto, getPhoto
from flag.gallery.models import Photo
from flask_paginate import Pagination #pip install -U flask-paginate
from PIL import Image #pip install pillow
from flask_login import login_required, current_user
#import boto

UPLOAD_FOLDER = 'flag/static/uploads/'
ALLOWED_IMAGE_EXTENSIONS = ["JPEG", "JPG", "PNG", "GIF"] #, "HEIC"

def get_pagePhotos(allPhotos, offset=0, per_page=6):
    return allPhotos[offset: offset + per_page]

@bpGallery.route('/gallery')
def gallery():
    try:
        filterBy = request.args.get('filter', 'A')
        userEmail = ''
        if filterBy == 'U':
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login', next=request.path + "?filter=U"))
            userEmail = current_user.email

        photoList= getPhotos(filterBy, userEmail) #currently we get all pages from database
        pageNumber = int(request.args.get('page', 1))    
        recordsPerPage = 6 #get from config
        offset = (pageNumber - 1) * recordsPerPage
        total = len(photoList)
        pagination_photos = get_pagePhotos(photoList,offset,recordsPerPage)
        pagination = Pagination(page=pageNumber, per_page=recordsPerPage, total=total, css_framework='bootstrap4')
        return render_template('gallery/gallery.html', 
                            photoList=pagination_photos,
                            page=pageNumber,
                            per_page=recordsPerPage,
                            pagination=pagination,
                            filterBy=filterBy)

    except Exception as e:
        app.logger.error(str(e), extra={'user': ''})
        return redirect(url_for('errors.error'))

@bpGallery.route('/uploadPhoto', methods=['GET', 'POST'])
@login_required
def uploadPhoto():
    try: 
        if request.method == 'POST':
            photoTitle = request.form['photoTitle']
            imageFile = request.files['inputImg']

            if imageFile.filename == "":
                print("No filename")
                return redirect(url_for('gallery.gallery', filter='U'))

            if allowed_image(imageFile.filename):
                filename = secure_filename(imageFile.filename)
    
            i = 0
            fileExistsName = filename
            while os.path.exists(os.path.join(UPLOAD_FOLDER, fileExistsName)):
                i += 1
                fileExistsName = filename.replace('.',  '_' + str(i) + '.')
            
            if fileExistsName != filename:
                filename = filename.replace('.', '_' + str(i) + '.') #add number at end of file to make unique and not replace previous uploaded ones.

            imageFile.save(os.path.join(UPLOAD_FOLDER, filename))
            # i = open(os.path.join(UPLOAD_FOLDER, filename), 'rb')
            # idata = i.read()
            # i.close

            fix_orientation(os.path.join(UPLOAD_FOLDER, filename))

            photo = Photo(0, photoTitle, filename, None, current_user.email) #, idata)

            savePhoto(photo) #save to database
            return redirect(url_for('gallery.gallery', filter='U')) #reload gallery page
    except Exception as e:
        app.logger.error(str(e), extra={'user': ''})
        return redirect(url_for('errors.error'))


@bpGallery.route('/deletePhoto/<id>')
@login_required
def removePhoto(id):
    try: 
        photo = getPhoto(id)
        print(id + photo.photoFileName)
        os.remove(os.path.join(UPLOAD_FOLDER, photo.photoFileName)) #remove file
        deletePhoto(id) #remove from database
        return redirect("/gallery") #reload gallery page
    except Exception as e:
        app.logger.error(str(e), extra={'user': ''})
        return redirect(url_for('errors.error'))

#private methods

def allowed_image(filename):
    # We only want files with a . in the filename
    if not "." in filename:
        return False
    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]
    # Check if the extension is in ALLOWED_IMAGE_EXTENSIONS
    if ext.upper() in ALLOWED_IMAGE_EXTENSIONS:
        return True
    else:
        return False


def fix_orientation(filename):
    img = Image.open(filename)
    if hasattr(img, '_getexif'):
        exifdata = img._getexif()
        try:
            orientation = exifdata.get(274)
        except:
            # There was no EXIF Orientation Data
            orientation = 1
    else:
        orientation = 1

    #, expand=True -> optional param to keep original size
    if orientation is 1:    # Horizontal (normal)
        return
    elif orientation is 2:  # Mirrored horizontal
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif orientation is 3:  # Rotated 180
        img = img.rotate(180, expand=True)
    elif orientation is 4:  # Mirrored vertical
        img = img.rotate(180, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
    elif orientation is 5:  # Mirrored horizontal then rotated 90 CCW
        img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
    elif orientation is 6:  # Rotated 90 CCW
        img = img.rotate(-90, expand=True)
    elif orientation is 7:  # Mirrored horizontal then rotated 90 CW
        img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
    elif orientation is 8:  # Rotated 90 CW
        img = img.rotate(90, expand=True)

    #save the result and overwrite the originally uploaded image
    img.save(filename)
from flask import render_template, redirect, url_for, request, flash, redirect
from flag.gallery import bpGallery
from flask import current_app as app

@bpGallery.route('/gallery')
def gallery(): 
    return render_template('gallery/gallery.html')
from flask import render_template, redirect, url_for, request, flash, redirect
from flag.sitecontent import bpSiteContent
from flag.sitecontent.models import SiteContent
from flag.dataaccess.siteContentDAO import getSiteContents, saveSiteContent, getSiteContent, updateSiteContent, deleteSiteContent
from flag.sitecontent.forms import SiteContentForm
import datetime
from flask_login import login_required, current_user
from flask import current_app as app

@bpSiteContent.route('/sitecontents')
@login_required
def sitecontents():
    if current_user.userRole != 'A':
        app.logger.error('Unauthorized!!!!', extra={'user': current_user.email})
        return redirect(url_for('errors.error'))
    siteContentList= getSiteContents()
    return render_template('sitecontent/sitecontents.html', siteContentList = siteContentList)

@bpSiteContent.route('/sitecontent/<siteContent_id>', methods=('GET', 'POST'))
@login_required
def sitecontent(siteContent_id = 0):
    if current_user.userRole != 'A':
        app.logger.error('Unauthorized!!!!', extra={'user': current_user.email})
        return redirect(url_for('errors.error'))
    
    form = SiteContentForm(request.form)

    if request.method == "GET":
        form.siteContentId.data = siteContent_id
        if int(form.siteContentId.data) > 0:
            siteContent = getSiteContent(siteContent_id)
            form.siteContentTitle.data = siteContent.siteContentTitle
            form.siteContentDesc.data = siteContent.siteContentDesc

    if request.method == "POST":
        if form.validate() == False:
            return render_template('sitecontent/sitecontent.html',form = form) 
        #save to db
        try:
            isHtml = 'N'
            if "<p" in form.siteContentDesc.data or "<br" in form.siteContentDesc.data or "<div" in form.siteContentDesc.data or "<img" in form.siteContentDesc.data:
                isHtml = 'Y'
            content = SiteContent(form.siteContentId.data, form.siteContentTitle.data, form.siteContentDesc.data, isHtml)
            if int(form.siteContentId.data) > 0:
                updateSiteContent(content)
            else:
                saveSiteContent(content)
            return redirect("/sitecontents") #go to siteamic contents page
        except Exception as e:
            print('failed.....' + e.args )

    return render_template('sitecontent/sitecontent.html',form = form)

@bpSiteContent.route('/removeSiteContent/<siteContent_id>')
@login_required
def removeSiteContent(siteContent_id = 0):
    if current_user.userRole != 'A':
        app.logger.error('Unauthorized!!!!', extra={'user': current_user.email})
        return redirect(url_for('errors.error'))
    deleteSiteContent(siteContent_id)
    return redirect("/sitecontents") #reload page

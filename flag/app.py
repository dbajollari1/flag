from flask import Flask, render_template, request, redirect, url_for, flash, session, redirect   
from flag import create_app, db
from flag.dataaccess.home import getUpcomingEvent
from flag.events.models import Event

app = create_app()

@app.route('/')
@app.route('/home')
def home():
    try:
        event = getUpcomingEvent()
        return render_template('index.html', event = event)
    except Exception as e:
        app.logger.error(str(e), extra={'user': ''})
        return redirect(url_for('errors.error'))

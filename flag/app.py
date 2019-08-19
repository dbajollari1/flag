from flask import Flask, render_template, request, redirect, url_for, flash, session, redirect
from flag.config import Config
#from flask_mail import Mail
import logging
import logging.handlers
from flag.dataaccess.events import getUpcomingEvent
from flag.events.models import Event

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']
#mail = Mail(app)

from flag.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from flag.public import bp as public_bp
app.register_blueprint(public_bp)

from flag.events import bpEvents as events_bp
app.register_blueprint(events_bp)

from flag.gallery import bpGallery as gallery_bp
app.register_blueprint(gallery_bp)

from flag.auth import bpAuth as auth_bp
app.register_blueprint(auth_bp)

#setup logger
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(user)s : %(message)s [in %(pathname)s:%(lineno)d in %(funcName)s]')
handler = logging.handlers.RotatingFileHandler('flag.log', maxBytes=1024 * 1024, backupCount=3)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

@app.route('/')
@app.route('/home')
def home():
    event = getUpcomingEvent()
    return render_template('index.html', event = event)



from flask import Flask, render_template, request, redirect, url_for, flash, session, redirect
from flag.config import Config
import logging
import logging.handlers
from flag.dataaccess.homeDAO import getUpcomingEvent
from flag.events.models import Event
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = app.config['SECRET_KEY']

    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from flag.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from flag.auth import bpAuth as auth_bp
    app.register_blueprint(auth_bp)

    from flag.sitecontent import bpSiteContent as siteContent_bp
    app.register_blueprint(siteContent_bp)

    from flag.membership import bpMembership as membership_bp
    app.register_blueprint(membership_bp)

    from flag.public import bp as public_bp
    app.register_blueprint(public_bp)

    from flag.events import bpEvents as events_bp
    app.register_blueprint(events_bp)

    from flag.gallery import bpGallery as gallery_bp
    app.register_blueprint(gallery_bp)


    #setup logger
    app.logger = logging.getLogger(__name__)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(user)s : %(message)s [in %(pathname)s:%(lineno)d in %(funcName)s]')
    #write to error file (flag.log) handler
    handler = logging.handlers.RotatingFileHandler('flag.log', maxBytes=1024 * 1024, backupCount=3)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    with app.app_context():
	    db.create_all()

    return app

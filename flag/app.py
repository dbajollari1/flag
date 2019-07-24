from flask import Flask, render_template, request, redirect, url_for, flash, session, redirect
from flag.config import Config
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']
mail = Mail(app)

from flag.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from flag.public import bp as public_bp
app.register_blueprint(public_bp)

from flag.events import bpEvents as events_bp
app.register_blueprint(events_bp)

from flag.gallery import bpGallery as gallery_bp
app.register_blueprint(gallery_bp)


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')



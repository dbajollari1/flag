from flask import Blueprint

bpEvents = Blueprint('events', __name__)

from flag.events import routes

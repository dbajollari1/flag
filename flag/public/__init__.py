from flask import Blueprint

bp = Blueprint('public', __name__)

from flag.public import routes

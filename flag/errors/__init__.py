from flask import Blueprint

bp = Blueprint('errors', __name__)

from flag.errors import handlers

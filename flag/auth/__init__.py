from flask import Blueprint

bpAuth = Blueprint('auth', __name__)

from flag.auth import routes
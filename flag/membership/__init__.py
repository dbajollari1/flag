from flask import Blueprint

bpMembership = Blueprint('membership', __name__)

from flag.membership import routes

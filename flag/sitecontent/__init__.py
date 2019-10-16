from flask import Blueprint

bpSiteContent = Blueprint('sitecontent', __name__)

from flag.sitecontent import routes

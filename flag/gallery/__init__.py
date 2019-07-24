from flask import Blueprint

bpGallery = Blueprint('gallery', __name__)

from flag.gallery import routes
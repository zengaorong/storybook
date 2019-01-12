from flask import Blueprint

story = Blueprint('story', __name__)

from . import views

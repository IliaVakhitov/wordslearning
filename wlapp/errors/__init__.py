from flask import Blueprint

bp = Blueprint('errors', __name__)

from wlapp.errors import handlers

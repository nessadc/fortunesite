from flask import Blueprint

bp = Blueprint('errors', __name__)

from fortunesite.errors import handlers

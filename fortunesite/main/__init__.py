from flask import Blueprint

bp = Blueprint('main', __name__)

from fortunesite.main import routes

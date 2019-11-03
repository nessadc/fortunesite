from flask import Blueprint

bp = Blueprint('auth', __name__)

from fortunesite.auth import routes

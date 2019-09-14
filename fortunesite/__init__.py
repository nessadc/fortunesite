from flask import Flask

app = Flask(__name__)

from fortunesite import routes

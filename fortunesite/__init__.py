from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '8OG$FGd9j&QF0sfwwdIf'

from fortunesite import routes

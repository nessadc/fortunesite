from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

sql_uri = '/Users/nessad/Programming/fortunesite/fortunesite/site.db'

app = Flask(__name__)
app.config['SECRET_KEY'] = '8OG$FGd9j&QF0sfwwdIf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + sql_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from fortunesite import routes

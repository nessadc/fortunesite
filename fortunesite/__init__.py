from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

sql_uri = '/Users/device42/programming/fortunesite/fortunesite/site.db'

app = Flask(__name__)
app.config['SECRET_KEY'] = '8OG$FGd9j&QF0sfwwdIf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + sql_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from fortunesite import routes

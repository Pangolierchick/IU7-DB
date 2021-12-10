from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from main import *

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:198011901@localhost/db_labs'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

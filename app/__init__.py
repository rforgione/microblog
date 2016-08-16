from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# in each of our submodules (views, models, etc.) the first thing that
# we do is import the app object from the app package. if we imported
# these packages before we define the app variable, the variable wouldn't
# exist yet, and we'd get an import error. that's why the import has to
# be *after* the app variable is set to a Flask object.
from app import views, models

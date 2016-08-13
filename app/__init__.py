from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
# importing the views module from the app package requires that the 'app'
# variable be defined, i.e., there MUST be a variable named app containing a
# Flask object.
from app import views

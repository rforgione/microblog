#!flask/bin/python

# from the app variable defined in __init__.py, we import the app variable,
# which contains the main Flask object for the application.
from app import app
app.run(debug=True)

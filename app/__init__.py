# Import flask and template operators
from flask import Flask, render_template
from flask_cors import CORS
from flask_marshmallow import Marshmallow
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)
CORS(app)

# Configs
app.config.from_envvar('FLASK_CONFIG')

# Define the database object which is imported
# by modules and controllers.py
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    print(error)
    return render_template('404.html'), 404


# Import a module / component using its blueprint handler variable
@app.route('/')
def default_page():
    return "This is default page, nothing here yet"


from app.users.controllers import users as users_module
from app.suites.controllers import suites as suites_module

# Register blueprint(s)
app.register_blueprint(users_module)
app.register_blueprint(suites_module)
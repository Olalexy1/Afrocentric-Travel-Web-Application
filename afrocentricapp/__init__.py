from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_wtf.csrf import CSRFProtect

#Instantiate an object of flask
app = Flask(__name__, instance_relative_config=True)
csrf = CSRFProtect(app)

#Local imports start here
from afrocentricapp import config
app.config.from_object(config.ProductionConfig)
#load below the config from instance folder
app.config.from_pyfile('config.py', silent=False)

db = SQLAlchemy(app)

#Load your routes/views
from afrocentricapp.myroutes import adminroutes, userroutes #since routes is now a module of its own
from afrocentricapp import forms, mymodels
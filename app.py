#!/usr/bin/env python3 

# Importing the necessary modules 
import os 
import logging 
from flask import Flask, url_for, session 
from flask_cors import CORS 
from datetime import timedelta 
from dotenv import load_dotenv 

# loading the env 
load_dotenv()

# Importing the views 
from Home.routes import home
from Register.routes import register
from About.routes import about

# Creating the flask application 
app = Flask(__name__, static_folder=None, template_folder=None) 
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = os.getenv('SECRET_KEY')
app.permanent_session_lifetime = timedelta(days=24)

# Setting the cors application 
CORS(app)

# Register the views using the "app.register" function 
app.register_blueprint(home, url_prefix="/")
app.register_blueprint(about, url_prefix="/about")
app.register_blueprint(register, url_prefix="/register")

# Running the flask application 
if __name__ == "__main__":
    app.run(port=5001, 
            host="localhost",
            debug=True
    ) 
    # Running the application   
    app.run() 
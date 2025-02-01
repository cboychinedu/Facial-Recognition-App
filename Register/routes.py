#!/usr/bin/env python3

# Importing the necessary modules 
import os 
from flask import request 
from flask import Blueprint 
from flask import session, flash 
from flask import render_template, redirect, url_for 

# Creating the blueprint object 
register = Blueprint('register', __name__, template_folder='templates', static_folder='static')

# Creating the home page 
@register.route('/', methods=['POST', 'GET'])
def RegisterPage():
    # Rendering the html template file 
    return render_template('register.html')
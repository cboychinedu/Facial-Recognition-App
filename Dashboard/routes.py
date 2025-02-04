#!/usr/bin/env python3 

# Importing the necessary modules 
import os 
import json 
from flask import request, Blueprint, session, redirect, jsonify, url_for, render_template

# Creating the blueprint object 
dashboard = Blueprint('dashboard', __name__, 
                      template_folder='templates', 
                      static_folder='static')

# Creating the dashboard home page 
@dashboard.route('/', methods=['GET'])
def Dashboard(): 
    # Checking if the user is logged in 
    if 'email' in session: 
        email = session['email']

        # Render the dashboard page 
        return render_template('Dashboard.html')
    
    # if the user email wasn't found 
    else: 
        # Redirecting the user back to the home page 
        return redirect(url_for('home.HomePage')); 
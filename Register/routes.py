#!/usr/bin/env python3

# Importing the necessary modules 
import os 
import sqlite3 
from flask import request, jsonify
from flask import Blueprint 
from flask import session, flash 
from flask import render_template, redirect, url_for 

# Setting the path to the database 
databasePath = os.sep.join(['Database', 'database.db'])

# Connecting to the database 
conn = sqlite3.connect(databasePath, check_same_thread=False) 

# Creating the blueprint object 
register = Blueprint('register', __name__, template_folder='templates', static_folder='static')

# Creating the home page 
@register.route('/', methods=['POST', 'GET'])
def RegisterPage():
    # Checking if the user is logged in 
    if 'email' in session: 
        email = session['email']

        # render the dashboard page 
        return render_template('dashboard.html')
    
    # Checking if the request was made to a post request 
    if request.method == 'POST': 
        # Getting the firstname, lastname, email and password 
        requestData = request.get_json()
        firstname = requestData['firstname'] 
        lastname = requestData['lastname']
        emailAddress = requestData['emailAddress']
        password = requestData['password']

        # Creating the cursor 
        cursor = conn.cursor()

        # Checking if the user is already registered on the database 
        cursor.execute("SELECT * FROM users WHERE emailAddress = ?", (emailAddress,))
        user = cursor.fetchall() 

        # If the user exists on the database, execute the block of code 
        # below 
        if user: 
            # 
            return jsonify({
                "status": "error", 
                "message": "The user already exists on the database"
            }), 404
        
        else: 
            # Save the user on the database 
            cursor.execute("""
                INSERT INTO users (firstname, lastname, emailAddress, password)
                VALUES (?, ?, ?, ?)""", (firstname, lastname, emailAddress, password))
            
            # Commit the changes 
            conn.commit() 

            # return the success message 
            return jsonify({
                "status": "success", 
                "message": "User registered successfully",
            }), 201 



    # Rendering the html template file 
    return render_template('register.html')
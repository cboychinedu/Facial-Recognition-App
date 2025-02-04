#!/usr/bin/env python3 

# Importing the necessary modules 
import os 
import sqlite3 
import bcrypt
from flask import request, Blueprint, session, jsonify, render_template, redirect, url_for

# Setting the path to the database 
databasePath = os.sep.join(['Database', 'database.db'])

# Connecting to the database 
conn = sqlite3.connect(databasePath, check_same_thread=False)

# Creating the blueprint object 
home = Blueprint('home', __name__, template_folder='templates', static_folder='static'); 

# Creating the home page 
@home.route("/", methods=["GET", "POST"])
def HomePage():
    # Checking if the user is logged in 
    if 'email' in session: 
        email = session['email']

        # render the dashboard page 
        return redirect(url_for('dashboard.Dashboard'))
    
    # Checking if the request was a post request 
    if request.method == 'POST': 
        # Getting the email, and password data from the 
        # request data available in the submitted html form 
        requestData = request.get_json() 
        emailAddress = requestData['emailAddress']
        password = requestData['password'] 

        # Getting the user's data by connecting to the 
        # sqlite database 
        cursor = conn.cursor() 

        # Get the user from the database 
        cursor.execute("SELECT emailAddress, password FROM users WHERE emailAddress = ?", (emailAddress,))
        user = cursor.fetchall() 

        # if the user exists on the database 
        if user: 
            # execute the block of code below if the user 
            # exists on the database 
            passwordCondition = bcrypt.checkpw(password.encode('utf-8'), user[0][1].encode('utf-8'))
            
            # Checking if the password condition returned a True value 
            if (passwordCondition == True): 
                # Give the user a sessions value, and redirect the user to the 
                # dashboard page 
                session['email'] = emailAddress

                # Creating the success message 
                successMessage = {
                    "status": "success", 
                    "message": "User logged in", 
                    "statusCode": 200, 
                }

                # Sending the success message 
                return jsonify(successMessage)
            
            # if the password condition was False 
            elif (passwordCondition == False): 
                # Creating the error message 
                errorMessage = {
                    "status": "error", 
                    "message": "Invalid username, or password", 
                    "statusCode": 500, 
                }

                # Sending the error message 
                return jsonify(errorMessage)

        # Else if the user was found on the database  
        else: 
            # Creating an error message 
            errorMessage = {
                "status": "error", 
                "message": "User not found on the database", 
                "statusCode": 501, 
            }

            # Returning the database data 
            return jsonify(errorMessage); 



    # Rendering the html template file 
    return render_template('home.html'); 


# creating the logout route 
@home.route('/logout', methods=['GET'])
def Logout(): 
    # Remoing the email from the session storage 
    session.pop('email', None); 

    # Redirecting the user back to the home page 
    return redirect(url_for('home.HomePage'))
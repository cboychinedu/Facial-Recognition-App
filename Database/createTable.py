#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('database.db')

conn.execute('''CREATE TABLE users(
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        emailAddress TEXT NOT NULL, 
        password TEXT NOT NULL);''')

conn.close()
from flask import Flask, request, jsonify
import database
import uuid

def add_user():
    conn = database.get_connection()
    if conn != None:  # Checking if connection is None
        if conn.is_connected() and request.method == 'POST':  # Checking if connection is established
            email = request.form.get("email")
            password = request.form.get("password")
            full_name = request.form.get("full_name")
            role = request.form.get("role")
            print(email,password,full_name, role, "\n\n\n" )
            dbcursor = conn.cursor()
            dbcursor.execute("INSERT INTO Users (email, password, full_name, role) VALUES (%s, %s, %s, %s)", (email,password,full_name, role,))
            conn.commit()
            dbcursor.close()
            conn.close()
            return "Ok"
        else:
            return "error connecting to db"
    else:
        return "error connecting to db"

def get_users():
    conn = database.get_connection()
    if conn != None:  # Checking if connection is None
        if conn.is_connected() and request.method == 'GET':  # Checking if connection is established
            dbcursor = conn.cursor()
            dbcursor.execute('SELECT * FROM Users')
            details = dbcursor.fetchall()
            conn.commit()
            dbcursor.close()
            conn.close()
            for x in range(len(details)):
                details[x] = {
                    "email": details[x][0],
                    "password": details[x][1],
                    "full_name": details[x][2],
                    "role": details[x][3],
                }
            if(details == None):
                return "No users"
            else:
                return jsonify({'users': details})
                   
        else:
            return "error connecting to db"
    else:
        return "error connecting to db"
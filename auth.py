from flask import Flask, request, jsonify
import database
import uuid

def login():
    conn = database.get_connection()
    if conn != None:  # Checking if connection is None
        if conn.is_connected() and request.method == 'GET':  # Checking if connection is established
            email = request.args.get("email")
            password = request.args.get("password")
            dbcursor = conn.cursor()
            dbcursor.execute('SELECT role FROM Users WHERE email =%s AND password =%s', (email,password,))
            role = dbcursor.fetchone()
            conn.commit()
            dbcursor.close()
            conn.close()
            if(role == None):
                return "Not found"
            else:
                session = str(uuid.uuid4())
                return jsonify({'sessionId': session, 'role': role})
        else:
            return "error connecting to db"
    else:
        return "error connecting to db"

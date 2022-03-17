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
            dbcursor.execute('SELECT email, password, full_name, role FROM Users WHERE email =%s AND password =%s', (email,password,))
            details = dbcursor.fetchone()
            conn.commit()
            dbcursor.close()
            conn.close()
            if(details == None):
                return "Not found"
            else:
                session = uuid.uuid4()
                return str(session)
        else:
            return "error connecting to db"
    else:
        return "error connecting to db"
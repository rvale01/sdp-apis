from flask import Flask, request, jsonify
import database
import uuid

def rooms_list():
    conn = database.get_connection()
    if conn != None:  # Checking if connection is None
        if conn.is_connected() and request.method == 'GET':  # Checking if connection is established
            dbcursor = conn.cursor()
            dbcursor.execute('SELECT * FROM room')
            details = dbcursor.fetchall()
            conn.commit()
            dbcursor.close()
            conn.close()
            for x in range(len(details)):
                details[x] = {
                    "room_id": details[x][0],
                    "patient_id": details[x][1],
                    "staff_email": details[x][2],
                }
            if(details == None):
                return "Not found"
            else:
                return jsonify({'rooms': details})
        else:
            return "error connecting to db"
    else:
        return "error connecting to db"

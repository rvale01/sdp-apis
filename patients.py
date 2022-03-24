from flask import Flask, request, jsonify
import database
import uuid

def patients_list():
    conn = database.get_connection()
    if conn != None:  # Checking if connection is None
        if conn.is_connected() and request.method == 'GET':  # Checking if connection is established
            dbcursor = conn.cursor()
            dbcursor.execute('SELECT * FROM patients')
            details = dbcursor.fetchall()
            conn.commit()
            dbcursor.close()
            conn.close()
            for x in range(len(details)):
                details[x] = {
                    "id": details[x][0],
                    "full_name": details[x][1],
                    "admission_date": details[x][2],
                    "estimated_leave_date": details[x][3],
                    "medication_needed": details[x][4],
                    "last_medicated": details[x][5],
                    "allergies": details[x][6],
                    "awaiting_tests": details[x][7],
                    "test_reviewed": details[x][8],
                    "emergency_contact": details[x][9],
                    "resuscitation_preference": details[x][10],
                }
            if(details == None):
                return "No patients"
            else:
                return jsonify({'patients_list': details})
                   
        else:
            return "error connecting to db"
    else:
        return "error connecting to db"

# single patient details

# rooms -> can only be seen by users

# account details
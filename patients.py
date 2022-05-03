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
                    "referral": details[x][11],
                    "csv_data": details[x][12],
                }
            if(details == None):
                return "No patients"
            else:
                return jsonify({'patients_list': details})
                   
        else:
            return "error connecting to db"
    else:
        return "error connecting to db"

def get_patients_data():
    conn = database.get_connection()
    if conn != None:  # Checking if connection is None
        if conn.is_connected() and request.method == 'GET':  # Checking if connection is established
            dbcursor = conn.cursor()
            dbcursor.execute('SELECT * FROM patients WHERE referral = 0')
            not_referral = dbcursor.fetchall()
            dbcursor.execute('SELECT * FROM patients WHERE referral = 1')
            referral = dbcursor.fetchall()
            return jsonify({'need_referral': referral, 'no_need_referral': not_referral})
        else:
            return "error connecting to db"
    else:
        return "error connecting to db"

def set_referred():
    conn = database.get_connection()
    if conn != None:  # Checking if connection is None
        if conn.is_connected() and request.method == 'POST':  # Checking if connection is established
            id = request.args.get("id")
            dbcursor = conn.cursor()
            dbcursor.execute('UPDATE patients SET referral = 0 WHERE (patient_id = %s)', (id,))
            conn.commit()
            dbcursor.close()
            conn.close()
            return "Okay"
        else:
            return "error connecting to db"
    else:
        return "error connecting to db"
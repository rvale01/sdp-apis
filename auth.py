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

def create_patient(full_name,
            admission_date,
            estimated_leave_date,
            medication_needed,
            last_medicated,
            allergies,
            awaiting_tests,
            test_reviewed,
            emergency_contact,
            resuscitation_preference,
            referred,
            csv_data):
    vars = locals()
    args = []
    for i in vars:
        if(str(i) == "csv_data"):
            for e in vars[i]:
                args.append(str(e))
        else:
            args.append(str(vars[i]))
    print(args)
    conn = database.get_connection()
    if conn != None:
        dbcursor = conn.cursor()
        # Not pretty but it works
        query = f"""
            INSERT INTO patients (full_name, admission_date, estimated_leave_date, medication_needed, last_medicated, allergies, awaiting_tests, test_reviewed, emergency_contact, resuscitation_preference, referral, end_tidal_co2, feed_vol, feed_vol_adm, fio2, fio2_ratio, insp_time, oxygen_flow_rate, peep, pip, resp_rate, sip, tidal_vol, tidal_vol_actual, tidal_vol_kg, tidal_vol_spon, bmi)
            VALUES ('{args[0]}', '{args[1]}', '{args[2]}', '{args[3]}', '{args[4]}', '{args[5]}', '{args[6]}', '{args[7]}', '{args[8]}', '{args[9]}', '{args[10]}', '{args[11]}', '{args[12]}', '{args[13]}', '{args[14]}', '{args[15]}', '{args[16]}', '{args[17]}', '{args[18]}', '{args[19]}', '{args[20]}', '{args[21]}', '{args[22]}', '{args[23]}', '{args[24]}', '{args[25]}', '{args[26]}');
        """
        print(query)
        dbcursor.execute(query)
        conn.commit()
        dbcursor.close()
        conn.close()

def edit_patient(patient_id,
            full_name=None,
            admission_date=None,
            estimated_leave_date=None,
            medication_needed=None,
            last_medicated=None,
            allergies=None,
            awaiting_tests=None,
            test_reviewed=None,
            emergency_contact=None,
            resuscitation_preference=None,
            referred=None,
            csv_data=None):
    vars = locals()
    args = ""
    for i in vars:
        if vars[i] != None:
            if(str(i) == "csv_data"):
                args += data_to_columns(vars[i])
            else:
                args += str(i) + "=" + "'" + str(vars[i]) + "', "
    conn = database.get_connection()
    if conn != None:
        dbcursor = conn.cursor()
        query = f"""
            UPDATE patients
            SET {args[args.find(",") + 2:-2]}
            WHERE patient_id = '{patient_id}';
        """
        dbcursor.execute(query)
        conn.commit()
        dbcursor.close()
        conn.close()

def data_to_columns(csv_data):
    #Assuming data is complete
    names = ["end_tidal_co2",
    "feed_vol",
    "feed_vol_adm",
    "fio2",
    "fio2_ratio",
    "insp_time",
    "oxygen_flow_rate",
    "peep",
    "pip",
    "resp_rate",
    "sip",
    "tidal_vol",
    "tidal_vol_actual",
    "tidal_vol_kg",
    "tidal_vol_spon",
    "bmi"]
    output = ""
    for i, e in zip(csv_data, names):
        output += str(e) + " = '" + i + "', "
    return output

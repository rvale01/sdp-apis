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

def create_user(email, hpasswd, full_name, role):
    conn = database.get_connection()
    if conn != None:
        dbcursor = conn.cursor()
        query = """INSERT INTO Users
            VALUES (%s, %s, %s, %s);"""
        data = (email, hpasswd, full_name, role)
        dbcursor.execute(query, data)
        conn.commit()
        dbcursor.close()
        conn.close()
        return True
    return False

def get_patients(email):
    conn = database.get_connection()
    if conn != None:
        dbcursor = conn.cursor()
        query = f"""
            SELECT * FROM patients
            INNER JOIN patient_staff ON patients.patient_id=patient_staff.patient_id
            WHERE patient_staff.staff_email='{email}'"""
        dbcursor.execute(query)
        data = dbcursor.fetchall()
        dbcursor.close()
        conn.close()
        return data
    return None

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
    args = ""
    vars = locals()
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
            SET {args[args.find(",") + 2:-11]}
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
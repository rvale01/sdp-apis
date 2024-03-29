from flask import Flask, request, jsonify
import database 
import json
import datetime

def upload_csv():
    conn = database.get_connection()
    if conn != None:  # Checking if connection is None
        if conn.is_connected() and request.method == 'POST':  # Checking if connection is established
            dbcursor = conn.cursor()
            data = json.loads(request.data)['file']
            dbcursor.execute('DELETE FROM room WHERE room_id > 0')
            dbcursor.execute('DELETE FROM patients WHERE patient_id > 0')
            # assuming that the staff already exists
            # not handling if the staff_email does not exist
            for x in range(1, len(data)):
                dbcursor.execute(
                    "INSERT INTO patients \
                        (patient_id, full_name, admission_date, estimated_leave_date, \
                        medication_needed, last_medicated, allergies, awaiting_tests,\
                        test_reviewed, emergency_contact, resuscitation_preference, referral,\
                        end_tidal_co2, feed_vol, feed_vol_adm, fio2, \
                        fio2_ratio, insp_time, oxygen_flow_rate, peep, \
                        pip, resp_rate, sip, tidal_vol, \
                        tidal_vol_actual, tidal_vol_kg, tidal_vol_spon, bmi\
                        ) VALUES \
                        (%s, %s, %s, %s, \
                        %s, %s, %s, %s, \
                        %s, %s, %s, %s, \
                        %s, %s, %s, %s, \
                        %s, %s, %s, %s, \
                        %s, %s, %s, %s, \
                        %s, %s, %s, %s)", \
                            (data[x][0], data[x][2],  data[x][3],  data[x][4], \
                            data[x][5],  data[x][6],  data[x][7],  data[x][8],  \
                            data[x][9],  data[x][10],  data[x][11],  data[x][12], \
                            data[x][13],  data[x][14], data[x][15],  data[x][16], \
                            data[x][17],  data[x][18], data[x][19],  data[x][20], \
                            data[x][21],  data[x][22], data[x][23], data[x][24], \
                            data[x][25],  data[x][26], data[x][27], data[x][28],
                            ))
                dbcursor.execute("INSERT INTO room (patient_id, staff_email) VALUES (%s, %s)", (data[x][0], data[x][1]))

            conn.commit()
            dbcursor.close()
            conn.close()
            return "okay"
        else:
            return "error connecting to db"
    else:
        return "error connecting to db"

def add_patient():
    data = str(request.data).split(",")
    data[0] = data[0][2:]
    data[len(data) - 1] = data[len(data) - 1][:-1]
    conn = database.get_connection()
    if conn != None:  # Checking if connection is None
        if conn.is_connected() and request.method == 'POST':  # Checking if connection is established
            dbcursor = conn.cursor()
            id_str = str(datetime.datetime.timestamp(datetime.datetime.now()))
            id = int(id_str[5:10])
            print(id)
            dbcursor.execute(
                "INSERT INTO patients \
                    (patient_id, full_name, admission_date, estimated_leave_date, \
                    medication_needed, last_medicated, allergies, awaiting_tests,\
                    test_reviewed, emergency_contact, resuscitation_preference, referral,\
                    end_tidal_co2, feed_vol, feed_vol_adm, fio2, \
                    fio2_ratio, insp_time, oxygen_flow_rate, peep, \
                    pip, resp_rate, sip, tidal_vol, \
                    tidal_vol_actual, tidal_vol_kg, tidal_vol_spon, bmi\
                    ) VALUES \
                    (%s, %s, %s, %s, %s, \
                    %s, %s, %s, %s, \
                    %s, %s, %s, %s, \
                    %s, %s, %s, %s, \
                    %s, %s, %s, %s, \
                    %s, %s, %s, %s, \
                    %s, %s, %s)", \
                        (id, data[0], data[1], data[2],  data[3],  data[4], \
                        data[5],  data[6],  data[7],  data[8],  \
                        data[9],  data[10],  data[11],  data[12], \
                        data[13],  data[14], data[15],  data[16], \
                        data[17],  data[18], data[19],  data[20], \
                        data[21],  data[22], data[23], data[24], \
                        data[25],  data[26]
                        ))
            dbcursor.execute("INSERT INTO room (patient_id, staff_email) VALUES (%s, %s)", (id, data[27]))

            conn.commit()
            dbcursor.close()
            conn.close()
            return "okay"
        else:
            return "error connecting to db"
    else:
        return "error connecting to db"
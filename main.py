from flask import Flask, request, jsonify

import auth
import patients
import users
import upload
import rooms

app = Flask(__name__)

app.secret_key = "SLpqCzm8MSBDFJlVCjRL8dnw075SQzWW"
DB_NAME = 'akxgfb7wff6k2npl'

@app.route("/login", methods=['GET'])
def login():
    return auth.login()

@app.route("/patients-list", methods=['GET'])
def patients_list():
    return patients.patients_list()

@app.route("/patients-data", methods=['GET'])
def patients_data():
    return patients.get_patients_data()

@app.route("/get-users", methods=['GET'])
def get_users():
    return users.get_users()

@app.route("/add-user", methods=['POST'])
def add_user():
    return users.add_user()

@app.route("/upload-csv", methods=['POST'])
def upload_csv():
    return upload.upload_csv()

@app.route('/rooms-list', methods=['GET'])
def get_user_role():
    return rooms.rooms_list()

if __name__ == '__main__':
    app.run(debug=True)
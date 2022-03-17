from flask import Flask, request, jsonify

import auth

app = Flask(__name__)

app.secret_key = "SLpqCzm8MSBDFJlVCjRL8dnw075SQzWW"
DB_NAME = 'akxgfb7wff6k2npl'

@app.route("/login", methods=['GET'])
def login():
    return auth.login()

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify, send_from_directory
from generator import generate_password, generate_key
from database import save_credentials, retrieve_credentials, init_db
import os

app = Flask(__name__)

# Initialize the database
init_db()

# Key used to encrypt/decrypt passwords
key = generate_key()

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    user_data = data.get('user_data', '')
    password = generate_password(length=64, user_data=user_data)
    return jsonify({"password": password})

@app.route('/save', methods=['POST'])
def save():
    data = request.json
    site = data['site']
    username = data['username']
    password = data['password']
    save_credentials(site, username, password, key)
    return jsonify({"status": "success"})

@app.route('/retrieve', methods=['GET'])
def retrieve():
    credentials = retrieve_credentials(key)
    return jsonify({"credentials": credentials})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify
from flask_cors import CORS
from scalper import get_tickets

app = Flask(__name__)
CORS(app)

@app.route('/api/get_tickets', methods=['GET'])
def get_tickets_controller():
    tickets = get_tickets()
    return jsonify([ticket.__dict__ for ticket in tickets])

@app.route('/api/get_counter', methods=['GET'])
def get_counter():
    global counter
    return jsonify({"count": counter})
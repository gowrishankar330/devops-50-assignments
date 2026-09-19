# app-data/main.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify(status="ok", service="dataapp"), 200

@app.route("/data/report")
def report():
    return jsonify(team="data", report=[1, 2, 3]), 200

# app/main.py
from flask import Flask, jsonify, request
from prometheus_client import Counter, generate_latest
import os, signal
app = Flask(__name__)
requests_total = Counter("app_requests_total", "Total requests")
items = {}

@app.route("/crash", methods=["POST"])
def crash():
    print("simulating crash — SIGQUIT to gunicorn master", flush=True)
    os.kill(os.getppid(), signal.SIGQUIT)
    return "dying", 500

@app.route("/")
def index():
    return jsonify(app="devops-50-assignments", endpoints=["/health", "/metrics", "/items"]), 200

healthy = True  # module level, near `items = {}`

@app.route("/health")
def health():
    if not healthy:
        return jsonify(status="unhealthy"), 500
    return jsonify(status="ok"), 200

@app.route("/break", methods=["POST"])
def break_app():
    global healthy
    healthy = False
    print("app is now lying — process alive, health failing", flush=True)
    return jsonify(status="broken"), 200

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain"}

@app.route("/items", methods=["GET", "POST"])
def items_route():
    requests_total.inc()
    if request.method == "POST":
        data = request.get_json()
        items[data["id"]] = data
        return jsonify(data), 201
    return jsonify(list(items.values())), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory('web', 'index.html')

@app.route("/areas")
def areas():
    return send_from_directory('.', 'areas.json')

@app.route("/<path:path>")
def web(path):
    return send_from_directory('web', path)

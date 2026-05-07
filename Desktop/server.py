"""
Serwer:
    - wystawia endpoint /tasks, który zwraca listę komend do wykonania
    - wystawia endpoint /completed, który przyjmuje wyniki wykonania komend
    
    flask --app server run --debug
"""

from flask import Flask, request

app = Flask(__name__)

@app.route("/tasks", methods=["GET"])
def tasks():
    return {"cmd": "whoami"}

@app.route("/completed", methods=["POST"])
def completed():
    print(request.json["stdout"])
    return "gitówa", 200
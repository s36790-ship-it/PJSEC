"""
Serwer:
    - wystawia endpoint /a/tasks, który zwraca listę komend do wykonania
    - wystawia endpoint /a/result, który przyjmuje wyniki wykonania komend

    flask --app server run --debug
"""

from flask import Flask, request

from utils import ValidationError
from models import Task, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

with app.app_context():
    db.create_all()

# CLIENT ENDPOINTS
@app.route("/c/tasks", methods=["POST"])
def client_send_task():
    task = request.json
    try:
        task_instance = Task(type=task.get("type", None), cmd=task.get("cmd", None))
        task_instance.validate()
    except ValidationError as e:
        return e, 400
    db.session.add(task_instance)
    db.session.commit()
    db.session.refresh(task_instance)
    task["id"] = task_instance.id
    return task

@app.route("/c/tasks/<id>", methods=["GET"])
def client_get_task(id: int):
    task = db.get_or_404(Task, id)
    return {"id": task.id, "type": task.type, "cmd": task.cmd, "completed": task.completed, "result": task.result}

# AGENT ENDPOINTS
@app.route("/a/tasks", methods=["GET"])
def agent_get_pending_task():
    task = db.session.execute(db.select(Task).filter_by(completed=False)).scalars().first()
    if task:
        return {"id": task.id, "type": task.type, "cmd": task.cmd}
    return "No tasks", 404

@app.route("/a/result", methods=["POST"])
def agent_post_result():
    task = None
    if request.json["id"]:
        task = db.get_or_404(Task, request.json["id"])
    task.completed = True
    task.result = request.json["stdout"]
    db.session.commit()
    return "gitówa", 200

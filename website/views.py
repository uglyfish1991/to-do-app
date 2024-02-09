from flask import Blueprint, redirect, render_template, url_for, request
from .models import Todo
from . import db

my_view = Blueprint("my_view", __name__)

@my_view.route("/")
def home():
    todo_list = Todo.query.all()
    message = request.args.get('message', None)
    return render_template("page1.html",todo_list=todo_list, message=message)

@my_view.route("/add", methods=["POST"])
def add():
    try:
        task = request.form.get("task")
        new_todo = Todo(task=task)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("my_view.home"))
    except:
        message = "There was an error adding your task"
        return redirect(url_for("my_view.home", message=message))

@my_view.route("/update/<todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("my_view.home"))

@my_view.route("/edit/<todo_id>", methods=["GET","POST"])
def edit(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()

    if request.method == "POST":
        todo.task = request.form.get("editted_task")
        db.session.commit()
        return redirect(url_for("my_view.home"))
    return render_template("edit.html", todo=todo)

@my_view.route("/delete/<todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("my_view.home"))
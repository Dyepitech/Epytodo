from app import app
from flask import render_template, session
from flask import jsonify
from flask import Flask, request
import pymysql as sql
from app import controller
from app import models


@app.route('/', methods=['GET'])
def route_index():
    return models.main_page()


@app.route('/register', methods=['POST', 'GET'])
def route_register():
    if request.method == "POST":
        try:
            data = controller.user_sql(json_data=request.json, form_data=request.form)
            return models.create_user(data)
        except:
            return jsonify(error="internal error")
    else:
        return render_template("register.html")


@app.route('/login', methods=['POST', 'GET'])
def route_login():
    if request.method == "POST":
        try:
            data = controller.user_sql(json_data=request.json, form_data=request.form)
            return models.check_user(data)
        except:
            return (jsonify(error="internal error"), models.main_page())
    else:
        return render_template("login.html")


@app.route('/task', methods=['GET'])
def route_user_task():
    try:
        return models.display_all_task()
    except:
        return jsonify(error="internal error")


@app.route('/delete/task/<id_task>', methods=['POST'])
def route_user_task_del(id_task):
    try:
        return models.task_delete(id_task=id_task)
    except:
        return jsonify(error="internal error")


@app.route('/todo', methods=['POST', 'GET'])
def route_addtask():
    if request.method == "POST":
        try:
            data = controller.task_sql(json_data=request.json, form_data=request.form)
            return models.create_task(data=data)
        except Exception as e:
            print(e)
            return jsonify(error="internal error")
    else:
        return render_template("todo.html")

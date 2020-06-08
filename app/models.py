from app import app
from flask import render_template, url_for, jsonify, request
import pymysql as sql
from config import *

connect = sql.connect(host=DATABASE_HOST,
                      db=DATABASE_NAME,
                      user=DATABASE_USER,
                      password=DATABASE_PASS,
                      unix_socket=DATABASE_SOCK)
cursor = connect.cursor()

user_data = None
task_data = None


def create_user(data):
    global user_data
    exist = cursor.execute("SELECT * FROM user WHERE username='{}' AND password='{}';".format(data.get('username'),
                                                                                              data.get('password')))
    if exist > 0:
        user_data = data
        return (jsonify(error="Choose another username"), main_page())
    else:
        cursor.execute("INSERT INTO user (username, password) VALUES ('{}', '{}');".format(data.get('username'),
                                                                                           data.get('password')))
        connect.commit()
        return (jsonify(result="Account Created Succesfully"), main_page())


def check_user(data):
    global user_data
    empty = cursor.execute("SELECT * FROM user WHERE username='{}' AND password='{}';".format(data.get('username'),
                                                                                              data.get('password')))
    if empty > 0:
        user_data = data
        connect.commit()
        return (jsonify(result="Login successful"), main_page())
    else:
        return (jsonify(error="[Error] Login"), main_page())


def create_task(data):
    global user_data
    global task_data
    if user_data == None:
        return (jsonify(error="[Error] You must be login"), login_page())
    cursor.execute(
        "INSERT INTO task (title, description, begin, end, status) VALUES ('{}', '{}', '{}', '{}', '{}');".format(
            data.get('title'),
            data.get('description'),
            data.get('begin'),
            data.get('end'),
            data.get('status')))
    connect.commit()
    return (jsonify(result="[Result]Your task has been added"), main_page())


def display_all_task():
    global task_data
    global user_data
    if user_data == None:
        return (jsonify(error="[Error] You must be login"), login_page())
    result = ''
    cursor.execute("SELECT * FROM task;")
    result = cursor.fetchall()
    task_data = {"tasks":{t_id: {"title":title, "description":description, "begin":str(begin), "end":str(end), "status":status} for t_id, title, description, begin, end, status in result}}
    data = {"tasks":[{t_id: {"title":title, "description":description, "begin":str(begin), "end":str(end), "status":status}} for t_id, title, description, begin, end, status in result]}
    return(jsonify(result=data), main_page())


def main_page():
    return render_template("index.html",
                           user_data=user_data,
                           task_data=task_data)
def login_page():
    return render_template("login.html",
                           user_data=user_data,
                           task_data=task_data)

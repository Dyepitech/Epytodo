from app import app
from flask import render_template
from flask import jsonify
from flask import Flask, request
import pymysql as sql


def user_sql(json_data, form_data):
    if type(json_data) is dict:
        data = json_data
    else:
        data = {"username": form_data['username'], "password": form_data['password']}
    return data


def task_sql(json_data, form_data):
    if type(json_data) is dict:
        data = json_data
    else:
        data = {"title": form_data['taskname'], "description": form_data['taskdes'], "begin": form_data['start'],
                "end": form_data['end'],
                "status": form_data['gridRadios']}
        print(data)
    return data

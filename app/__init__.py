from flask import Flask

app = Flask(__name__)
app.secret_key = 'dev'

app.config.from_object('config')
from app import views

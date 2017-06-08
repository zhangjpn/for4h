#-*- coding:utf-8 -*-

from flask import Flask
from .views import init_views

def create_app():
    app = Flask(__name__)
    app.config['MONGODB_DB'] = 'for4h'
    app.config['MONGODB_HOST'] = '127.0.0.1'
    app.config['MONGODB_PORT'] = 27017
    init_views(app)
    return app
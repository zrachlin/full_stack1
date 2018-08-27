# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 11:22:19 2018

@author: zrachlin
"""

import os
from flask import Flask

def create_app(test_config=None):
    #creates and configures the app -> this is the app factory
    
    #creates the Flask instance, __name__ is the name of the current python module - helps with path setup
    app = Flask(__name__, instance_relative_config=True) 
    app.config.from_mapping(
            SECRET_KEY='dev', #override with random value when deploying
            DATABASE=os.path.join(app.instance_path,'flaskBlog.sqlite'))
    
    if test_config is None:
        #load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py',silent=True)
    else:
        #load the test config if passed in
        app.config.from_mapping(test_config)
    
    #ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    #simple greeting page
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/',endpoint='index')
    
    return app

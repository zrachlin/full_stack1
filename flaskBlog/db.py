# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 11:41:55 2018

@author: zrachlin

From http://flask.pocoo.org/docs/1.0/tutorial/database/:
    g is a special object that is unique for each request. It is used to store 
    data that might be accessed by multiple functions during the request. 
    The connection is stored and reused instead of creating a new connection 
    if get_db is called a second time in the same request.

    current_app is another special object that points to the Flask application 
    handling the request. Since you used an application factory, there is no 
    application object when writing the rest of your code. get_db will be 
    called when the application has been created and is handling a request, 
    so current_app can be used.
    
    sqlite3.connect() establishes a connection to the file pointed at by the 
    DATABASE configuration key. This file doesn’t have to exist yet, and won’t 
    until you initialize the database later.

    sqlite3.Row tells the connection to return rows that behave like dicts. 
    This allows accessing the columns by name.

    close_db checks if a connection was created by checking if g.db was set. 
    If the connection exists, it is closed. Further down you will tell your 
    application about the close_db function in the application factory so 
    that it is called after each request.
"""

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
        
    return g.db

def close_db(e=None):
    db = g.pop('db',None)
    
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
        
@click.command('init-db')
@with_appcontext
def init_db_command():
    '''clears the existing data and creates new tables'''
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    


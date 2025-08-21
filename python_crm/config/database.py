"""Database configuration for the Python CRM application."""

import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

def init_db(app: Flask):
    """Initialize the database with the Flask app."""
    # Database configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'elie')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'joseph')
    DB_NAME = os.getenv('DB_NAME', 'my_db')
    
    # MySQL connection string
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    return db
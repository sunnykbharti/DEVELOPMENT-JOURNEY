from flask import Flask, request, redirect, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demo.db'

db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    gender = db.Column(db.String(10), nullable = False)
    contact = db.Column(db.String(15), nullable = False)

    def __repr__(self) : 
        return f'<Patient {self.anme}>'

import datetime

from flask import Flask, render_template, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from factory import LoadBlueprints
from database import db, Produkt


app = Flask(__name__, static_url_path='/static/admin')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///allgoldDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'wfsd54"§%df4r4'

#create database
db.init_app(app)



with app.app_context():
    db.create_all()


#Load Blueprints
LoadBlueprints(app)

if __name__ == '__main__':
    app.run(debug = True)


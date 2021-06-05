from flask import Flask, render_template, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static/admin')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#create database
db = SQLAlchemy(app)

def LoadBlueprints(app):
    from index.view import Index
    from lieferant.view import Lieferant
    from geschaeftsfuehrer.view import Geschaeftsfuehrer


    app.register_blueprint(Index)
    app.register_blueprint(Lieferant)
    app.register_blueprint(Geschaeftsfuehrer, url_prefix="/geschaeftsfuehrer")


LoadBlueprints(app)

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)


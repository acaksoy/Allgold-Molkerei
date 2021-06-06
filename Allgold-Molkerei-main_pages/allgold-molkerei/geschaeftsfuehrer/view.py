from flask import Blueprint, render_template, request,flash, redirect
from .form import verkaufStelleForm
from flask_sqlalchemy import SQLAlchemy
from database import Verkaufstelle
from database import db


Geschaeftsfuehrer = Blueprint('geschaeftsfuehrer', __name__, template_folder='pages', static_folder='static')

# all routes
@Geschaeftsfuehrer.route('/', methods=['GET','POST'])
def home():

    return render_template('geschaeftsfuehrer.html')

@Geschaeftsfuehrer.route('/neuVerStl', methods=['GET','POST']) # sadece POSTla olmuyor. ya GET ve POST bir arada kullanilacak ya da ikisi de kullanilmayacak.
def neuVerkaufStelle():
    if request.method == "POST":
        verkaufstelle = Verkaufstelle(request.form['name'], request.form['typ'])
        db.session.add(verkaufstelle)
        db.session.commit()
        flash("New markt added to dataASS")
        return render_template("test.html", verkst = verkaufstelle)

    return render_template('Erstellen.html')

@Geschaeftsfuehrer.route('/uebersicht', methods=['GET','POST'])
def uebersicht():

    return render_template('uebersicht.html')

@Geschaeftsfuehrer.route('/bearbeiten', methods=['GET','POST']) # sadece POSTla olmuyor. ya GET ve POST bir arada kullanilacak ya da ikisi de kullanilmayacak.
def bearbeiten():

    return render_template('bearbeiten.html')
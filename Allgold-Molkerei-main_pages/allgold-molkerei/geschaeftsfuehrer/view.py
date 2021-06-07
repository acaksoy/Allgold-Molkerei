from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import Verkaufstelle, Adresse, Inventar, Produkt
from database import db



Geschaeftsfuehrer = Blueprint('geschaeftsfuehrer', __name__, template_folder='pages', static_folder='static')

# all routes
@Geschaeftsfuehrer.route('/', methods=['GET','POST'])
def home():
    if request.method == "GET":
        alleVerkaufstelle = Verkaufstelle.query.all()

        return render_template('geschaeftsfuehrer.html', alleVerkaufstelle = alleVerkaufstelle)

@Geschaeftsfuehrer.route('/preisliste', methods=['GET','POST'])
def preisliste():

    alleProdukte = Produkt.query.all()
    return render_template('preisliste.html', alleProdukte = alleProdukte)

@Geschaeftsfuehrer.route('prodHinz', methods = ['GET', 'POST'])
def neuProd():
    if request.method == "POST":

        date1 = datetime.strptime(request.form['vrDat'], '%Y-%m-%d').date()
        prod = Produkt(request.form['name'], request.form['preis'], date1)
        db.session.add(prod)
        db.session.commit()
        flash("Produkt gespeichert", "success")
        return redirect(url_for(".home", prod=prod))
    return render_template('produktHinz.html')

@Geschaeftsfuehrer.route('/neuVerStl', methods=['GET','POST']) # sadece POSTla olmuyor. ya GET ve POST bir arada kullanilacak ya da ikisi de kullanilmayacak.
def neuVerkaufStelle():
    if request.method == "POST":
        nameInventar = "Inventar des " + request.form['name']
        inventar = Inventar(nameInventar)
        db.session.add(inventar)
        db.session.commit()

        adress = Adresse(request.form['hnr'], request.form['plz'], request.form['ort'], request.form['str'],
                         request.form['beschr'])
        db.session.add(adress)
        db.session.commit()

        neuVerkaufstelle = Verkaufstelle(request.form['name'], request.form['typ'], adress.adressID, inventar.inventarID)
        db.session.add(neuVerkaufstelle)
        db.session.commit()

        return redirect(url_for("geschaeftsfuehrer.home"))

    return render_template('Erstellen.html')

@Geschaeftsfuehrer.route('/uebersicht/<int:verkaufstelleID>', methods=['GET','POST'])
def uebersicht(verkaufstelleID):
    verkaufstelle = Verkaufstelle.query.get(verkaufstelleID)
    adresse = Adresse.query.get(verkaufstelle.adresse_ID)

    return render_template('uebersicht.html', verkaufstelle= verkaufstelle, adresse = adresse)

@Geschaeftsfuehrer.route('/bearbeiten/<int:verkaufstelleID>', methods=['GET','POST']) # sadece POSTla olmuyor. ya GET ve POST bir arada kullanilacak ya da ikisi de kullanilmayacak.
def bearbeiten(verkaufstelleID):
    if request.method == "GET":
        verkaufstelle = Verkaufstelle.query.get(verkaufstelleID)
        adresse = Adresse.query.get(verkaufstelle.adresse_ID)
        return render_template('bearbeiten.html', verkaufstelle= verkaufstelle, adresse = adresse)
    elif request.method == "POST":
        verkaufstelle = Verkaufstelle.query.get(verkaufstelleID)
        adresse = Adresse.query.get(verkaufstelle.adresse_ID)

        if request.form['name'] is not "":
            verkaufstelle.name = request.form['name']
        if request.form['typ'] is not "":
            verkaufstelle.typ = request.form['typ']
        db.session.merge(verkaufstelle)
        db.session.commit()

        if request.form['hnr'] is not "":
            adresse.hausNR = request.form['hnr']
        if request.form['ort'] is not "":
            adresse.ort = request.form['ort']
        if request.form['plz'] is not "":
            adresse.plz = request.form['plz']
        if request.form['str'] is not "":
            adresse.strasse = request.form['str']
        if request.form['beschr'] is not "":
            adresse.beschreibung = request.form['beschr']

        db.session.merge(adresse)
        db.session.commit()

        return redirect(url_for("geschaeftsfuehrer.uebersicht", verkaufstelleID =verkaufstelle.verkaufstelleID))

@Geschaeftsfuehrer.route('/loeschen/<int:verkaufstelleID>', methods=['GET','POST'])
def loeschen(verkaufstelleID):
    verkaufstelle = Verkaufstelle.query.get(verkaufstelleID)
    adresse = Adresse.query.get(verkaufstelle.adresse_ID)
    db.session.delete(adresse)
    db.session.delete(verkaufstelle)
    db.session.commit()

    return redirect(url_for("geschaeftsfuehrer.home"))
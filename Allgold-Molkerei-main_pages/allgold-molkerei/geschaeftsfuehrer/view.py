from flask import Blueprint, render_template, request, redirect, url_for
from database import Verkaufstelle, Adresse
from database import db



Geschaeftsfuehrer = Blueprint('geschaeftsfuehrer', __name__, template_folder='pages', static_folder='static')

# all routes
@Geschaeftsfuehrer.route('/', methods=['GET','POST'])
def home():
    if request.method == "GET":
        alleVerkaufstelle = Verkaufstelle.query.all()
        return render_template('geschaeftsfuehrer.html', alleVerkaufstelle = alleVerkaufstelle)




@Geschaeftsfuehrer.route('/neuVerStl', methods=['GET','POST']) # sadece POSTla olmuyor. ya GET ve POST bir arada kullanilacak ya da ikisi de kullanilmayacak.
def neuVerkaufStelle():
    if request.method == "POST":
        adress = Adresse(request.form['hnr'], request.form['plz'], request.form['ort'], request.form['str'],
                         request.form['beschr'])
        db.session.add(adress)
        db.session.commit()

        neuVerkaufstelle = Verkaufstelle(request.form['name'], request.form['typ'], adress.adressID)
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

        verkaufstelle.name = request.form['name']
        verkaufstelle.typ = request.form['typ']
        db.session.merge(verkaufstelle)
        db.session.commit()

        adresse.hausNR = request.form['hnr']
        adresse.ort = request.form['ort']
        adresse.plz = request.form['plz']
        adresse.strasse = request.form['str']
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
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, make_response,flash
from database import Verkaufstelle, Adresse, Inventar, Produkt, Lieferung, Elements
from database import db
import pdfkit



Geschaeftsfuehrer = Blueprint('geschaeftsfuehrer', __name__, template_folder='pages', static_folder='static')

# all routes
@Geschaeftsfuehrer.route('/', methods=['GET','POST'])
def home():
    if request.method == "POST":
        if Verkaufstelle.query.filter_by(name=request.form['search']).first() is  not None:
            verkaufstelle = Verkaufstelle.query.filter_by(name=request.form['search']).first()
            return render_template('search.html', verkaufstelle=verkaufstelle)
        else:
            alleVerkaufstelle = Verkaufstelle.query.all()
            return render_template('geschaeftsfuehrer.html', alleVerkaufstelle=alleVerkaufstelle)
    if request.method == "GET":
        alleVerkaufstelle = Verkaufstelle.query.all()
        return render_template('geschaeftsfuehrer.html', alleVerkaufstelle=alleVerkaufstelle)


@Geschaeftsfuehrer.route('/preisliste/<string:typ>', methods=['GET','POST'])
def liste(typ):
    if typ == "preisliste":
        alleProdukte = Produkt.query.all()
        return render_template('preisliste.html', alleProdukte=alleProdukte)
    if typ == "lieferungen":
        alleLieferungen = Lieferung.query.all()
        return render_template('lieferungen.html', alleLieferungen=alleLieferungen)


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

@Geschaeftsfuehrer.route('/createdPDF/<string:typ>/<int:verkaufstelleID>', methods=['GET','POST'])
def createPDF(typ, verkaufstelleID):
    rendered = None
    if typ == "preisliste":
        jedesElement= Produkt.query.all()
        rendered = render_template("preislistePDF.html", jedesElement=jedesElement)
    if typ == "lieferungen":
        jedesElement = Lieferung.query.all()
        rendered = render_template("lieferungenPDF.html", jedesElement=jedesElement)
    if typ == "inventar":
        verkstl = Verkaufstelle.query.get(verkaufstelleID)
        inventar = Inventar.query.get(verkstl.inventar_ID)
        jedesElement = Elements.query.filter_by(inventar_ID= inventar.inventarID).all()
        rendered = render_template("inventarPDF.html", jedesElement=jedesElement, verkstl= verkstl, inventar= inventar)

    config = pdfkit.configuration(wkhtmltopdf=r"C:\Programme\wkhtmltopdf\bin\wkhtmltopdf.exe")
    options = {"enable-local-file-access": None}


    pdf = pdfkit.from_string(rendered, False, configuration=config, options=options)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline;filename = output.pdf"
    return response


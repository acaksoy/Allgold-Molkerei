from datetime import datetime

import flask
from flask import Blueprint, render_template, request, redirect, url_for, make_response, flash
from database import Verkaufstelle, Adresse, Inventar, Produkt, Lieferung, Elements, Verkauf
from database import db
import pdfkit
import json

Geschaeftsfuehrer = Blueprint('geschaeftsfuehrer', __name__, template_folder='pages', static_folder='static')


# all routes
@Geschaeftsfuehrer.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        if Verkaufstelle.query.filter_by(name=request.form['search']).first() is not None:
            verkaufstelle = Verkaufstelle.query.filter_by(name=request.form['search']).first()
            return render_template('search.html', verkaufstelle=verkaufstelle)
        else:
            alleVerkaufstelle = Verkaufstelle.query.all()
            return render_template('geschaeftsfuehrer.html', alleVerkaufstelle=alleVerkaufstelle)
    if request.method == "GET":
        alleVerkaufstelle = Verkaufstelle.query.all()
        return render_template('geschaeftsfuehrer.html', alleVerkaufstelle=alleVerkaufstelle)


@Geschaeftsfuehrer.route('/preisliste/<string:typ>', methods=['GET', 'POST'])
def liste(typ):
    if typ == "preisliste":
        alleProdukte = Produkt.query.all()
        return render_template('preisliste.html', alleProdukte=alleProdukte)
    if typ == "lieferungen":
        alleLieferungen = Lieferung.query.all()
        return render_template('lieferungen.html', alleLieferungen=alleLieferungen)


@Geschaeftsfuehrer.route('prodHinz', methods=['GET', 'POST'])
def neuProd():
    if request.method == "POST":
        if request.form['vrDat'] == "":
            flash('Gültigen Datum eingeben!', 'error')
            return render_template('produktHinz.html')
        date1 = datetime.strptime(request.form['vrDat'], '%Y-%m-%d').date()
        prod = Produkt(request.form['name'], request.form['preis'], date1)
        db.session.add(prod)
        db.session.commit()
        flash("Produkt gespeichert", "success")
        return redirect(url_for(".home", prod=prod))
    return render_template('produktHinz.html')


@Geschaeftsfuehrer.route('/neuVerStl', methods=['GET',
                                                'POST'])  # sadece POSTla olmuyor. ya GET ve POST bir arada kullanilacak ya da ikisi de kullanilmayacak.
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

        neuVerkaufstelle = Verkaufstelle(request.form['name'], request.form['typ'], adress.adressID,
                                         inventar.inventarID)
        db.session.add(neuVerkaufstelle)
        db.session.commit()

        return redirect(url_for("geschaeftsfuehrer.home"))

    return render_template('Erstellen.html')


@Geschaeftsfuehrer.route('/uebersicht/<int:verkaufstelleID>', methods=['GET', 'POST'])
def uebersicht(verkaufstelleID):
    verkaufstelle = Verkaufstelle.query.get(verkaufstelleID)
    adresse = Adresse.query.get(verkaufstelle.adresse_ID)

    return render_template('uebersicht.html', verkaufstelle=verkaufstelle, adresse=adresse)


@Geschaeftsfuehrer.route('/bearbeiten/<int:verkaufstelleID>', methods=['GET',
                                                                       'POST'])  # sadece POSTla olmuyor. ya GET ve POST bir arada kullanilacak ya da ikisi de kullanilmayacak.
def bearbeiten(verkaufstelleID):
    if request.method == "GET":
        verkaufstelle = Verkaufstelle.query.get(verkaufstelleID)
        adresse = Adresse.query.get(verkaufstelle.adresse_ID)
        return render_template('bearbeiten.html', verkaufstelle=verkaufstelle, adresse=adresse)
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

        return redirect(url_for("geschaeftsfuehrer.uebersicht", verkaufstelleID=verkaufstelle.verkaufstelleID))


@Geschaeftsfuehrer.route('/loeschen/<int:verkaufstelleID>', methods=['GET', 'POST'])
def loeschen(verkaufstelleID):
    verkaufstelle = Verkaufstelle.query.get(verkaufstelleID)
    adresse = Adresse.query.get(verkaufstelle.adresse_ID)
    inventar = Inventar.query.get(verkaufstelle.inventar_ID)
    elements = Elements.query.filter_by(inventar_ID=verkaufstelle.inventar_ID).all()

    db.session.query(Verkauf).filter(Verkauf.verkaufstelleID==verkaufstelle.verkaufstelleID).delete()
    db.session.query(Lieferung).filter(Lieferung.verkaufstelleID==verkaufstelle.verkaufstelleID).delete()
    db.session.query(Elements).filter(Elements.inventar_ID==inventar.inventarID).delete()
    db.session.delete(inventar)
    db.session.delete(adresse)
    db.session.delete(verkaufstelle)


    db.session.commit()

    return redirect(url_for("geschaeftsfuehrer.home"))


@Geschaeftsfuehrer.route('/createdPDF/<string:typ>/<int:verkaufstelleID>', methods=['GET', 'POST'])
def createPDF(typ, verkaufstelleID):
    rendered = None
    if typ == "preisliste":
        jedesElement = Produkt.query.all()
        rendered = render_template("preislistePDF.html", jedesElement=jedesElement)
    if typ == "inventar":
        verkstl = Verkaufstelle.query.get(verkaufstelleID)
        inventar = Inventar.query.get(verkstl.inventar_ID)
        jedesElement = Elements.query.filter_by(inventar_ID=inventar.inventarID).all()
        rendered = render_template("inventarPDF.html", jedesElement=jedesElement, verkstl=verkstl, inventar=inventar)
    if typ == "verkauf":
        verkstl = Verkaufstelle.query.get(verkaufstelleID)
        verkaufen = Verkauf.query.filter_by(verkaufstelleID=verkaufstelleID).all()
        rendered = render_template("verkaufPDF.html", verkaufen=verkaufen, verkstl=verkstl)


    config = pdfkit.configuration(wkhtmltopdf=r"C:\Programme\wkhtmltopdf\bin\wkhtmltopdf.exe")
    options = {"enable-local-file-access": None}

    pdf = pdfkit.from_string(rendered, False, configuration=config, options=options)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline;filename = output.pdf"
    return response


@Geschaeftsfuehrer.route('/statistics', methods=['GET', 'POST'])
def statisticHTML():
    alleVerkaufstelle = Verkaufstelle.query.all()

    anzahlProdukt = Produkt.query.count()
    labels = []
    datas = {}
    totalMenge = 0
    allgemeinTotalMenge = 0
    allgemeinProduktVerkauf ={}
    for p in range(1, anzahlProdukt+1):
        produkt = Produkt.query.get(p)
        labels.append(produkt.name)
    for v in alleVerkaufstelle:
        vID = v.verkaufstelleID
        data = []
        for p in range(1, anzahlProdukt + 1):
            verkaufen = Verkauf.query.filter((Verkauf.produktID == p) & (Verkauf.verkaufstelleID == vID)).all()
            for verkauf in verkaufen:
                totalMenge = totalMenge + verkauf.verkaufMenge
            data.append(totalMenge)
            totalMenge = 0
        datas[v]=data
    for n in range(1, anzahlProdukt + 1):
        produkt = Produkt.query.get(n)
        name = produkt.name
        verkaufen = Verkauf.query.filter(Verkauf.produktID == n).all()
        for verkauf in verkaufen:
            allgemeinTotalMenge = allgemeinTotalMenge + verkauf.verkaufMenge
        allgemeinProduktVerkauf[name] = allgemeinTotalMenge
        allgemeinTotalMenge = 0

    # return flask.jsonify({'payload': json.dumps({'data': data, 'labels': labels})})
    return render_template("statistikenPDF.html", allgemeinProduktVerkauf=allgemeinProduktVerkauf, alleVerkaufstelle=alleVerkaufstelle, labels=labels, data=data, datas=datas)


@Geschaeftsfuehrer.route('/statistics/pdf')
def createStatisticPDF():
    alleVerkaufstelle = Verkaufstelle.query.all()

    anzahlProdukt = Produkt.query.count()
    labels = []
    data = []
    totalMenge = 0

    for p in range(1, anzahlProdukt + 1):
        produkt = Produkt.query.get(p)
        verkaufen = Verkauf.query.filter(Verkauf.produktID == p).all()
        labels.append(produkt.name)
        for verkauf in verkaufen:
            totalMenge = totalMenge + verkauf.verkaufMenge
        data.append(totalMenge)
        totalMenge = 0

    return flask.jsonify({'payload': json.dumps({'data': data, 'labels': labels})})

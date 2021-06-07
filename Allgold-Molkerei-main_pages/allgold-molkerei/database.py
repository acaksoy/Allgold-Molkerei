from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Adresse(db.Model):
    adressID = db.Column("adressID", db.Integer, primary_key=True)
    hausNR = db.Column(db.Integer)
    plz = db.Column(db.Integer)
    ort = db.Column(db.String(20))
    strasse = db.Column(db.String(50))
    beschreibung = db.Column(db.String(200))

    _verkaufstelle = db.relationship("Verkaufstelle", uselist=False, back_populates="_adresse")

    def __init__(self, hausNr, plz, ort, strasse, beschreibung):
        self.hausNR = hausNr
        self.plz = plz
        self.ort = ort
        self.strasse = strasse
        self.beschreibung = beschreibung


class Verkaufstelle(db.Model):
    verkaufstelleID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    typ = db.Column(db.String(30))

    adresse_ID = db.Column(db.Integer, db.ForeignKey('adresse.adressID'), nullable=False)
    _adresse = db.relationship("Adresse", back_populates="_verkaufstelle")

    def __init__(self, name, typ, adresse_ID):
        self.name = name
        self.typ = typ
        self.adresse_ID = adresse_ID



class Inventar(db.Model):
    inventarID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    prodMenge = db.Column(db.Integer)


    def __init__(self, name, prodMenge):
        self.name = name
        self.prodMenge = prodMenge



class Produkt(db.Model):
    produktID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    preis = db.Column(db.Integer)
    verfallsDatum = db.Column(db.DateTime)
    anschaffungsDatum = db.Column(db.DateTime)


    def __init__(self, name, preis, verfallsDatum, anschaffungsDatum):
        self.name = name
        self.preis = preis
        self.verfallsDatum = verfallsDatum
        self.anschaffungsDatum = anschaffungsDatum


class Lieferung(db.Model):
    lieferID = db.Column(db.Integer, primary_key=True)
    lieferDatum = db.Column(db.DateTime)
    lieferMenge = db.Column(db.Integer)
    verkstelleName = db.Column(db.String(50))


    def __init__(self, lieferDatum, lieferMenge, verkstelleName):
        self.lieferDatum = lieferDatum
        self.lieferMenge = lieferMenge
        self.verkstelleName = verkstelleName



class Verkauf(db.Model):
    verkaufID = db.Column(db.Integer, primary_key=True)
    verkaufDatum = db.Column(db.DateTime)
    verkaufMenge = db.Column(db.Integer)
    verkaufProduktName = db.Column(db.String(50))


    def __init__(self, verkaufDatum, verkaufMenge):
        self.verkaufDatum = verkaufDatum
        self.verkaufMenge = verkaufMenge


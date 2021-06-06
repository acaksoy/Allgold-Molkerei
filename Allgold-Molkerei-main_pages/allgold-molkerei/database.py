from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Adresse(db.Model):
    adressID = db.Column("adressID", db.Integer, primary_key=True)
    hausNR = db.Column(db.Integer)
    plz = db.Column(db.Integer)
    ort = db.Column(db.String(20))
    strasse = db.Column(db.String(50))
    beschreibung = db.Column(db.String(200))
    verkaufstelleID = db.Column(db.Integer, db.ForeignKey('verkaufstelle.verkaufstelleID'), nullable=False)

    def __init__(self, hausNr, plz, ort, strasse, beschreibung, verkaufstelleID):
        self.hausNR = hausNr
        self.plz = plz
        self.ort = ort
        self.strasse = strasse
        self.beschreibung = beschreibung
        self.verkaufstelleID = verkaufstelleID


class Verkaufstelle(db.Model):
    verkaufstelleID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    typ = db.Column(db.String(30))

    def __init__(self, name, typ):
        self.name = name
        self.typ = typ


class Inventar(db.Model):
    inventarID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    prodMenge = db.Column(db.Integer)
    verkaufstelleID = db.Column(db.Integer, db.ForeignKey('verkaufstelle.verkaufstelleID'), nullable=False)
    produktID = db.Column(db.Integer, db.ForeignKey('produkt.produktID'), nullable=False)

    def __init__(self, name, prodMenge, verkaufstelleID, produktID):
        self.name = name
        self.prodMenge = prodMenge
        self.verkaufstelleID = verkaufstelleID
        self.produktID = produktID



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
    adressID = db.Column(db.Integer, db.ForeignKey('adresse.adressID'), nullable=False)
    produktID = db.Column(db.Integer, db.ForeignKey('produkt.produktID'), nullable=False)
    verkaufstelleID = db.Column(db.Integer, db.ForeignKey('verkaufstelle.verkaufstelleID'), nullable=False)

    def __init__(self, lieferDatum, lieferMenge, verkstelleName, adressID,produktID,verkaufstelleID):
        self.lieferDatum = lieferDatum
        self.lieferMenge = lieferMenge
        self.verkstelleName = verkstelleName
        self.adressID = adressID
        self.produktID = produktID
        self.verkaufstelleID = verkaufstelleID


class Verkauf(db.Model):
    verkaufID = db.Column(db.Integer, primary_key=True)
    verkaufDatum = db.Column(db.DateTime)
    verkaufMenge = db.Column(db.Integer)
    verkaufProduktName = db.Column(db.String(50))
    produktID = db.Column(db.Integer, db.ForeignKey('produkt.produktID'), nullable=False)
    verkaufstelleID = db.Column(db.Integer, db.ForeignKey('verkaufstelle.verkaufstelleID'), nullable=False)

    def __init__(self, verkaufDatum, verkaufMenge, verkaufProduktName, produktID,verkaufstelleID):
        self.verkaufDatum = verkaufDatum
        self.verkaufMenge = verkaufMenge
        self.verkaufProduktName = verkaufProduktName
        self.produktID = produktID
        self.verkaufstelleID = verkaufstelleID

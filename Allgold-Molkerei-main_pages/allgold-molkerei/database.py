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

    inventar_ID = db.Column(db.Integer, db.ForeignKey('inventar.inventarID'), nullable=False)
    _inventar = db.relationship("Inventar", back_populates="_verkaufstelle")

    def __init__(self, name, typ, adresse_ID, inventar_ID):
        self.name = name
        self.typ = typ
        self.adresse_ID = adresse_ID
        self.inventar_ID = inventar_ID



class Inventar(db.Model):
    inventarID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    _verkaufstelle = db.relationship("Verkaufstelle", uselist=False, back_populates="_inventar")
    _elements = db.relationship("Elements")

    def __init__(self, name):
        self.name = name

class Elements(db.Model):
    elementID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    preis = db.Column(db.Integer)
    verfallsDatum = db.Column(db.Date)
    anschaffungsDatum = db.Column(db.Date)

    inventar_ID = db.Column(db.Integer, db.ForeignKey('inventar.inventarID'), nullable=False)
    produktID = db.Column(db.Integer, db.ForeignKey('produkt.produktID'), nullable=False)

    def __init__(self, produktID, inventar_ID, anschaffungsDatum):
        self.name = Produkt.query.get(produktID).name
        self.preis = Produkt.query.get(produktID).preis
        self.verfallsDatum =  Produkt.query.get(produktID).verfallsDatum
        self.anschaffungsDatum = anschaffungsDatum
        self.inventar_ID = inventar_ID


class Produkt(db.Model):
    produktID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    preis = db.Column(db.Integer)
    verfallsDatum = db.Column(db.Date)


    def __init__(self, name, preis, verfallsDatum):
        self.name = name
        self.preis = preis
        self.verfallsDatum = verfallsDatum



class Lieferung(db.Model):
    lieferID = db.Column(db.Integer, primary_key=True)
    lieferDatum = db.Column(db.Date)
    lieferMenge = db.Column(db.Integer)
    verkstelleName = db.Column(db.String(50))

    produktID = db.Column(db.Integer, db.ForeignKey('produkt.produktID'), nullable=False)
    verkaufstelleID = db.Column(db.Integer, db.ForeignKey('verkaufstelle.verkaufstelleID'), nullable=False)

    def __init__(self, lieferDatum, lieferMenge, verkstelleName, produktID, verkaufstelleID):
        self.lieferDatum = lieferDatum
        self.lieferMenge = lieferMenge
        self.verkstelleName = verkstelleName
        self.produktID = produktID
        self.verkaufstelleID = verkaufstelleID


class Verkauf(db.Model):
    verkaufID = db.Column(db.Integer, primary_key=True)
    verkaufDatum = db.Column(db.Date)
    verkaufMenge = db.Column(db.Integer)
    verkaufProduktName = db.Column(db.String(50))

    produktID = db.Column(db.Integer, db.ForeignKey('produkt.produktID'), nullable=False)
    verkaufstelleID = db.Column(db.Integer, db.ForeignKey('verkaufstelle.verkaufstelleID'), nullable=False)

    def __init__(self, verkaufDatum, verkaufMenge, produktID, verkaufstelleID):
        self.verkaufDatum = verkaufDatum
        self.verkaufMenge = verkaufMenge
        produkt = Produkt.query.get(produktID)
        self.verkaufProduktName = produkt.name
        self.produktID = produktID
        self.verkaufstelleID = verkaufstelleID

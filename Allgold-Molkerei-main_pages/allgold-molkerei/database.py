from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Adresse(db.Model):
    adressID = db.Column(db.Integer, primary_key=True)
    hausNR = db.Column(db.Integer)
    plz = db.Column(db.Integer)
    ort = db.Column(db.String(20))
    strasse = db.Column(db.String(50))
    beschreibung = db.Column(db.String(200))
    verkaufstelleID = db.Column(db.Integer, db.ForeignKey('verkaufstelle.verkaufstelleID'),nullable=False)



class Verkaufstelle(db.Model):
    verkaufstelleID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    typ = db.Column(db.Column(30))

class Inventar(db.Model):
    inventarID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    prodMenge =db.Column(db.Integer)
    verkaufstelleID = db.Column(db.Integer, db.ForeignKey('verkaufstelle.verkaufstelleID'),nullable=False)
    produktID = db.Column(db.Integer, db.ForeignKey('produkt.produktID'),nullable=False)

class Produkt(db.Model):
    produktID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    preis = db.Column(db.Integer)
    verfallsDatum = db.Column(db.DateTimeField)
    anschaffungsDatum = db.Column(db.DateTimeField)

class Lieferung(db.Model):
    lieferID = db.Column(db.Integer, primary_key=True)
    lieferDatum = db.Column(db.DateTimeField)
    lieferMenge = db.Column(db.Integer)
    verkstelleName = db.Column(db.String(50))
    adressID = db.Column(db.Integer, db.ForeignKey('adresse.adressID'),nullable=False)
    produktID = db.Column(db.Integer, db.ForeignKey('produkt.produktID'), nullable=False)
    verkaufstelleID = db.Column(db.Integer, db.ForeignKey('verkaufstelle.verkaufstelleID'), nullable=False)

class Verkauf(db.Model):
    verkaufID = db.Column(db.Integer, primary_key=True)
    verkaufDatum = db.Column(db.DateTimeField)
    verkaufMenge = db.Column(db.Integer)
    verkaufProduktName = db.Column(db.String(50))
    produktID = db.Column(db.Integer, db.ForeignKey('produkt.produktID'), nullable=False)
    verkaufstelleID = db.Column(db.Integer, db.ForeignKey('verkaufstelle.verkaufstelleID'), nullable=False)


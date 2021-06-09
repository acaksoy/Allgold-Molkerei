from flask import Blueprint, render_template,request, flash, redirect, url_for
from database import Elements, Verkauf,Produkt, db, Verkaufstelle,Inventar
from datetime import datetime
Verkaeufer = Blueprint('verkaeufer', __name__, template_folder='pages', static_folder='static', static_url_path='/verkaeufer/static')

# all routes
@Verkaeufer.route('/verkaeufer')
def home():

    return render_template('verkaeufer.html')

@Verkaeufer.route('/erfassen', methods=['GET','POST'])
def erfassen():
    if request.method == "POST":
       date = datetime.strptime(request.form['vkDat'], '%Y-%m-%d').date()
       menge = int(request.form['mg'])

       verkerf = Verkauf(date,request.form['mg'],request.form['prID'],int(request.form['vkID']))
       db.session.add(verkerf)
       db.session.commit()

       pID = int(request.form['prID'])
       verkstelle = Verkaufstelle.query.get(verkerf.verkaufstelleID)
       invID = verkstelle.inventar_ID
       INV = Inventar.query.get(invID)

       for x in range(menge):
            element = Elements.query.filter_by(inventar_ID = INV.inventarID, produktID = pID).first()
            db.session.delete(element)
            db.session.commit()


       return render_template("verkaeufer.html")
       #return redirect(url_for(".home", verkerf=verkerf))
    else:
       flash('Gültige Verkaufsstellen ID eingeben!', 'error')
    return render_template('verkerf.html')

@Verkaeufer.route('/verkaeufer/prodErfassen', methods=['GET','POST'])
def proderfassen():
    if request.method == "POST":
       date = datetime.strptime(request.form['anDat'], '%Y-%m-%d').date()
       menge = int(request.form['mg'])

       for x in range(menge):
           proderfassen = Elements( request.form['prID'], request.form['inID'],date)
           db.session.add(proderfassen)
           db.session.commit()

       flash("Lieferung erfolgreich erfasst")

       return redirect(url_for(".home", proderfassen=proderfassen))
    return render_template('proderf.html')



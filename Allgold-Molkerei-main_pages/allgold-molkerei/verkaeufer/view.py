from flask import Blueprint, render_template,request, flash
from database import Elements, Verkauf
from datetime import datetime
Verkaeufer = Blueprint('verkaeufer', __name__, template_folder='pages', static_folder='static', static_url_path='/verkaeufer/static')

# all routes
@Verkaeufer.route('/verkaeufer')
def home():

    return render_template('verkaeufer.html')

@Verkaeufer.route('/erfassen', methods=['GET','POST'])
def erfassen():
    if request.method == "POST" and request.form['vkID'] is not "":
       date = datetime.strptime(request.form['vkDat'], '%Y-%m-%d')
       verkerf = Verkauf(request.form['vkID'], request.form['prID'],request.form['mg'],date)
       db.session.add(verkerf)
       db.session.commit()
       flash("Lieferung erfolgreich erfasst")
       return redirect(url_for("verkaeufer.erfassen", verkerf=verkerf))
    else:
       flash("Gültige Verkaufsstellen ID eingeben!")
    return render_template('verkerf.html')

@Verkaeufer.route('/verkaeufer/prodErfassen')
def proderfassen():
    if request.method == "POST":
       date = datetime.strptime(request.form['lfDat'], '%Y-%m-%d')
       proderfassen = Elements(request.form['name'], date, request.form['mg'],  request.form['prID'],)
       db.session.add(lieferfass)
       db.session.commit()
       flash("Lieferung erfolgreich erfasst")
       return render_template("test1.html", proderfassen=proderfassen)
    return render_template('proderf.html')



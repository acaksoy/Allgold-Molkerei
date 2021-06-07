from flask import Blueprint, render_template, request, flash, redirect, url_for
from database import Lieferung
from datetime import datetime
from database import db

Lieferant = Blueprint('lieferant', __name__, template_folder='pages', static_folder='static')

# all routes
@Lieferant.route('/lieferant')
def home():
    return render_template('lieferant.html')

@Lieferant.route('/erfassen', methods=['GET','POST'])
def erfassung():
    if request.method == "POST":
       date = datetime.strptime(request.form['lfDat'], '%Y-%m-%d')
       lieferfass = Lieferung(date, request.form['mg'], request.form['name'], request.form['prID'], request.form['vkID'])
       db.session.add(lieferfass)
       db.session.commit()
       return redirect(url_for("lieferant.home"))
    return render_template('lieferf.html')



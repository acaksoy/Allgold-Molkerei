from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from database import Lieferung,db, Verkaufstelle, Verkauf, Produkt
from datetime import datetime
import pdfkit

Lieferant = Blueprint('lieferant', __name__, template_folder='pages', static_folder='static')

# all routes
@Lieferant.route('/lieferant')
def home():
    return render_template('lieferant.html')

@Lieferant.route('/erfassen', methods=['GET','POST'])
def erfassung():
    if request.method == "POST":
        vkIDexist = db.session.query(Verkaufstelle.verkaufstelleID).filter_by(verkaufstelleID = int(request.form['vkID'])).first()
        prIDexist = db.session.query(Produkt.produktID).filter_by(produktID = int(request.form['prID'])).first()
        if vkIDexist and prIDexist is not None:
            date = datetime.strptime(request.form['lfDat'], '%Y-%m-%d').date()
            lieferfass = Lieferung(date, request.form['mg'], request.form['prID'], request.form['vkID'])
            db.session.add(lieferfass)
            db.session.commit()
            return redirect(url_for("lieferant.home"))
        elif not prIDexist and not vkIDexist:
            flash('Produkt und Verkaufstelle existieren nicht!', 'error')
            return render_template('lieferf.html')
        elif not prIDexist:
            flash('Produkt existiert nicht!', 'error')
            return render_template('lieferf.html')
        elif not vkIDexist:
            flash('Verkaufstelle existiert nicht!', 'error')
            return render_template('lieferf.html')
    return render_template('lieferf.html')

@Lieferant.route('/createdPDF', methods=['GET','POST'])
def createPDF():
    lief = Lieferung.query.all()
    verk = Verkaufstelle.query.all()
    rendered = render_template("lieferungenPDF.html", lief=lief, verk=verk)

    config = pdfkit.configuration(wkhtmltopdf=r"C:\Programme\wkhtmltopdf\bin\wkhtmltopdf.exe")
    options = {"enable-local-file-access": None}

    pdf = pdfkit.from_string(rendered, False, configuration=config, options=options)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline;filename = output.pdf"
    return response

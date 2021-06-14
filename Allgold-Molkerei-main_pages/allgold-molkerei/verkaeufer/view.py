import pdfkit
from flask import Blueprint, render_template,request, flash, redirect, url_for, make_response
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
       vkIDexist = db.session.query(Verkaufstelle.verkaufstelleID).filter_by(verkaufstelleID=int(request.form['vkID'])).first()
       prIDexist = db.session.query(Produkt.produktID).filter_by(produktID=int(request.form['prID'])).first()
       anzElement = db.session.query(Elements.elementID).count()
       menge = int(request.form['mg'])
       if vkIDexist and prIDexist is not None: # Does the shop and the product exist?
           if anzElement - menge >= 0: # Are there enough elements in Elements table?
               date = datetime.strptime(request.form['vkDat'], '%Y-%m-%d').date()
               verkerf = Verkauf(date,menge,request.form['prID'],int(request.form['vkID']))
               db.session.add(verkerf)
               db.session.commit()

               pID = int(request.form['prID'])
               verkstelle = Verkaufstelle.query.get(verkerf.verkaufstelleID)
               invID = verkstelle.inventar_ID
               INV = Inventar.query.get(invID)

               for x in range(menge): # Remove Elements table with the amount of "mg"
                   element = Elements.query.filter_by(inventar_ID=INV.inventarID, produktID=pID).order_by(
                       Elements.elementID.desc()).first()
                   db.session.delete(element)
                   db.session.commit()
               return render_template("verkaeufer.html")
           else:
               flash('Nicht genügend Elemente auf Lager!', 'error')
               return render_template('verkerf.html')
       elif not prIDexist and not vkIDexist:
           flash('Produkt und Verkaufstelle existieren nicht!', 'error')
           return render_template('verkerf.html')
       elif not prIDexist:
           flash('Produkt existiert nicht!', 'error')
           return render_template('verkerf.html')
       elif not vkIDexist:
           flash('Verkaufstelle existiert nicht!', 'error')
           return render_template('verkerf.html')
    return render_template('verkerf.html')

@Verkaeufer.route('/verkaeufer/prodErfassen', methods=['GET','POST'])
def proderfassen():
    if request.method == "POST":
       invIDexist = db.session.query(Inventar.inventarID).filter_by(inventarID=int(request.form['inID'])).first()
       prIDexist = db.session.query(Produkt.produktID).filter_by(produktID=int(request.form['prID'])).first()
       if invIDexist and prIDexist is not None:
           date = datetime.strptime(request.form['anDat'], '%Y-%m-%d').date()
           menge = int(request.form['mg'])

           for x in range(menge):
               proderfassen = Elements( request.form['prID'], request.form['inID'],date)
               db.session.add(proderfassen)
               db.session.commit()

           flash('Produkte erfolgreich erfasst', 'success')
       elif not prIDexist and not invIDexist:
           flash('Produkt und Inventar existieren nicht!', 'error')
           return render_template('proderf.html')
       elif not prIDexist:
           flash('Produkt existiert nicht!', 'error')
           return render_template('proderf.html')
       elif not invIDexist:
           flash('Inventar existiert nicht!', 'error')
           return render_template('proderf.html')
       return redirect(url_for(".home", proderfassen=proderfassen))
    return render_template('proderf.html')

@Verkaeufer.route('/createdPDF/<string:typ>/<int:verkaufstelleID>', methods=['GET','POST'])
def createPDF(typ, verkaufstelleID):
    rendered = None
    if typ == "preisliste":
        jedesElement= Produkt.query.all()
        rendered = render_template("preislistePDF.html", jedesElement=jedesElement)


    config = pdfkit.configuration(wkhtmltopdf=r"C:\Programme\wkhtmltopdf\bin\wkhtmltopdf.exe")
    options = {"enable-local-file-access": None}


    pdf = pdfkit.from_string(rendered, False, configuration=config, options=options)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline;filename = output.pdf"
    return response


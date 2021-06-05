from flask import Blueprint, render_template, redirect, url_for

Index = Blueprint('index', __name__, template_folder='pages', static_folder='static')

@Index.route('/')
def home():

    return render_template('index.html')

#def GeschaeftsfuehrerHome():

    #return redirect(url_for('geschaeftsfuehrer.home'))
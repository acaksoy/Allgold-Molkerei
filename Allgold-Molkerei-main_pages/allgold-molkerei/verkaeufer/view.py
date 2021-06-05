from flask import Blueprint, render_template

Verkaeufer = Blueprint('verkaeufer', __name__, template_folder='pages', static_folder='static', static_url_path='/verkaeufer/static')

# all routes
@Verkaeufer.route('/verkaeufer')
def home():

    return render_template('verkaeufer.html')

@Verkaeufer.route('/verkaeufer/erfassen')
def erfassen():

    return render_template('verkerf.html')

@Verkaeufer.route('/verkaeufer/prodErfassen')
def proderfassen():

    return render_template('proderf.html')



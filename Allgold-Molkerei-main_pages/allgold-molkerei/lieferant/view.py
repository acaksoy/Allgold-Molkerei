from flask import Blueprint, render_template

Lieferant = Blueprint('lieferant', __name__, template_folder='pages', static_folder='static')

# all routes
@Lieferant.route('/lieferant')
def home():

    return render_template('lieferant.html')
from flask import Blueprint, render_template

Geschaeftsfuehrer = Blueprint('geschaeftsfuehrer', __name__, template_folder='pages', static_folder='static')


# all routes
@Geschaeftsfuehrer.route('/', methods=['GET','POST'])
def home():


    return "falan" #render_template('list_mz.html', stempel=stempel, mitarbeiterEvents=mitarbeiterEvents, latest=latest, info=session, user=current_user)
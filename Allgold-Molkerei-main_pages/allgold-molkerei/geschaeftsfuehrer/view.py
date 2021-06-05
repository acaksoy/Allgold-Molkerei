from flask import Blueprint, render_template

Geschaeftsfuehrer = Blueprint('geschaeftsfuehrer', __name__, template_folder='pages', static_folder='static', static_url_path='/static')

# all routes
@Geschaeftsfuehrer.route('/', methods=['GET','POST'])
def home():

    return render_template('geschaeftsfuehrer.html')

@Geschaeftsfuehrer.route('/neuVerStl', methods=['GET','POST']) # sadece POSTla olmuyor. ya GET ve POST bir arada kullanilacak ya da ikisi de kullanilmayacak.
def neuVerkaufStelle():

    return render_template('Erstellen.html')
from flask import Blueprint, render_template

Index = Blueprint('index', __name__, template_folder='pages', static_folder='static')

# all routes
@Index.route('/')
def home():

    return render_template('index.html')
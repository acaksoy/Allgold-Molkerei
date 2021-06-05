from flask import Flask, render_template, url_for, Blueprint
from database import db

app = Flask(__name__, static_url_path='/static/admin')
db.init_app(app)

def loadBlueprints(app):
    from index.view import Index
    from lieferant.view import Lieferant
    from geschaeftsfuehrer.view import Geschaeftsfuehrer


    app.register_blueprint(Index)
    app.register_blueprint(Lieferant)
    app.register_blueprint(Geschaeftsfuehrer, url_prefix="/geschaeftsfuehrer")


loadBlueprints(app)

if __name__ == '__main__':
    app.run(debug = True)


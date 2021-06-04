from flask import Flask, render_template, url_for, Blueprint


app = Flask(__name__, static_url_path='/static/admin')

def loadBlueprints(app):
    from index.view import Index
    from lieferant.view import Lieferant

    app.register_blueprint(Index)
    app.register_blueprint(Lieferant)

loadBlueprints(app)

if __name__ == '__main__':
    app.run(debug = True)


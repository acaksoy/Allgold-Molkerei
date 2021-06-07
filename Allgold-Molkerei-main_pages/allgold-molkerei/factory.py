def LoadBlueprints(app):
    from index.view import Index
    from lieferant.view import Lieferant
    from geschaeftsfuehrer.view import Geschaeftsfuehrer
    from verkaeufer.view import Verkaeufer


    app.register_blueprint(Index)
    app.register_blueprint(Lieferant, url_prefix="/lieferant")
    app.register_blueprint(Geschaeftsfuehrer, url_prefix="/geschaeftsfuehrer")
    app.register_blueprint(Verkaeufer, url_prefix="/verkaeufer")
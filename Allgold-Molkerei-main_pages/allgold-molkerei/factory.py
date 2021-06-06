def LoadBlueprints(app):
    from index.view import Index
    from lieferant.view import Lieferant
    from geschaeftsfuehrer.view import Geschaeftsfuehrer


    app.register_blueprint(Index)
    app.register_blueprint(Lieferant)
    app.register_blueprint(Geschaeftsfuehrer, url_prefix="/geschaeftsfuehrer")
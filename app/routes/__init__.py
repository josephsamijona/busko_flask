from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    # Importez vos routes ici
    from app.routes import patient_routes, finance_routes, stock_routes, rendezvous_routes, pharmacy_routes, lab_routes

    # Enregistrez les Blueprints ici
    app.register_blueprint(patient_routes.patient_bp)
    app.register_blueprint(finance_routes.finance_bp)
    app.register_blueprint(stock_routes.stock_bp)
    app.register_blueprint(rendezvous_routes.rendezvous_bp)
    app.register_blueprint(pharmacy_routes.pharmacy_bp)
    app.register_blueprint(lab_routes.lab_bp)

    return app

# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restful import Api

# Crée les instances des extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
api = Api()

def create_app():
    app = Flask(__name__)

    # Configurations de l'application
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialise les extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Importe les routes
    from app.routes import patient_routes, rendezvous_routes, stock_routes, finance_routes, pharmacy_routes, lab_routes, analytic, dashboard, setting, historique, histrdvous, prescription

    # Ajoute les blueprints (routes) à l'application
    app.register_blueprint(patient_routes)
    app.register_blueprint(rendezvous_routes)
    app.register_blueprint(stock_routes)
    app.register_blueprint(finance_routes)
    app.register_blueprint(pharmacy_routes)
    app.register_blueprint(lab_routes)
    app.register_blueprint(analytic)
    app.register_blueprint(dashboard)
    app.register_blueprint(historique)
    app.register_blueprint(histrdvous)
    app.register_blueprint(prescription)
    app.register_blueprint(setting)
   


    return app

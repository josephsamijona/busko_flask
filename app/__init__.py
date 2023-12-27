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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cliniclelabo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialise les extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Importe les routes
    
    from app.routes.patient_routes import patient_routes
    from app.routes.rendezvous_routes import rendezvous_routes
    from app.routes.finance_routes import finance_routes
    from app.routes.pharmacy_routes import pharmacy_routes
    from app.routes.lab_routes import lab_routes
    from app.routes.analytic import analytic
    from app.routes.dashboard import dashboard
    from app.routes.setting import setting
    from app.routes.historique import historique
    from app.routes.histrdvous import histrdvous
    from app.routes.prescription import prescription
    from app.routes.stock_routes import stock_routes

    
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

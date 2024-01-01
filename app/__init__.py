# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restful import Api
from .models import db, Utilisateur, Connexion, DossierMedical, HistoriquePatient, Inventaire, MouvementsInventaire, Fournisseurs, AlertesReapprovisionnement, Rendezvous, Factures, Revenus, Depenses, ExamensHemogramme, ExamenUrine, ExamensBiochimie, ExamensSelles, Serologie, FichesPrescription, Ventes, MouvementsMedicaments, AlertesReapprovisionnementPharmacie, HistoriqueRendezvous, HistoriqueDossiersMedicaux, HistoriqueFactures, HistoriqueMedicamentsPharmacie

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbcliniclabo.db'  # Utilisez SQLite pour simplifier
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db.init_app(app)
migrate = Migrate(app, db)
# Crée les instances des extensions
login_manager = LoginManager()

api = Api()

# Import your models
from .models import Utilisateur, Connexion, DossierMedical, HistoriquePatient, Inventaire, MouvementsInventaire, Fournisseurs, AlertesReapprovisionnement, Rendezvous, Factures, Revenus, Depenses, ExamensHemogramme, ExamenUrine, ExamensBiochimie, ExamensSelles, Serologie, FichesPrescription, Ventes, MouvementsMedicaments, AlertesReapprovisionnementPharmacie, HistoriqueRendezvous, HistoriqueDossiersMedicaux, HistoriqueFactures, HistoriqueMedicamentsPharmacie

# Additional configurations or routes can be added here


def create_app():
    app = Flask(__name__)

    # Configurations de l'application
    app.config['SECRET_KEY'] = 'your_secret_key_here'
     

    # Initialise les extensions
    
   
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
    from app.routes.loginsignup import loginsignup
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
    app.register_blueprint(loginsignup)
    app.register_blueprint(prescription)
    app.register_blueprint(setting)
    app.register_blueprint(loginsignup)
   


    return app

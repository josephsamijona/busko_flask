# auth_manager.py
from flask_login import LoginManager
from app.models import Utilisateur  # Assurez-vous d'importer le modèle Utilisateur

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    # Fonction pour charger l'utilisateur actuel
    return Utilisateur.query.get(int(user_id))

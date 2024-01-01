# app/routes/setting.py
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Configuration

# Créez un Blueprint pour les routes des paramètres
setting_bp = Blueprint('setting', __name__)

# settings.py

 

# Vous pouvez ajouter d'autres routes ou ressources pour la gestion des paramètres

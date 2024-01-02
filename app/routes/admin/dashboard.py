# app/routes/admin/dashboard.py
from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.models import Utilisateur, db
from datetime import datetime

# Créez un Blueprint pour les routes du tableau de bord
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/admin/dashboard')

# Route pour obtenir les informations du tableau de bord
@dashboard_bp.route('/info', methods=['GET'])
@login_required
def get_dashboard_info():
    # Assurez-vous que l'utilisateur actuel est un administrateur
    if current_user.Account_Type != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    # Exemple : Récupérez le nombre total d'utilisateurs de chaque type
    total_users = Utilisateur.query.count()
    total_patients = Utilisateur.query.filter_by(Account_Type='patient').count()
    total_doctors = Utilisateur.query.filter_by(Account_Type='doctor').count()
    total_nurses = Utilisateur.query.filter_by(Account_Type='nurse').count()

    # Exemple : Récupérez des statistiques générales supplémentaires selon les besoins

    # Construisez la réponse JSON
    dashboard_info = {
        'total_users': total_users,
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_nurses': total_nurses,
        # Ajoutez d'autres statistiques au besoin
    }

    return jsonify(dashboard_info), 200

# Vous pouvez ajouter d'autres routes ou ressources pour le tableau de bord

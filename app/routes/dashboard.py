# app/routes/dashboard.py
from flask import Blueprint

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard', methods=['GET'])
def get_dashboard_data():
    # Logique pour récupérer les données du tableau de bord depuis la base de données
    return "Données du tableau de bord"

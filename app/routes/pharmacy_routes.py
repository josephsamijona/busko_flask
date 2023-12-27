# app/routes/pharmacy_routes.py
from flask import Blueprint

pharmacy_routes = Blueprint('pharmacy', __name__)

@pharmacy_routes.route('/pharmacy', methods=['GET'])
def get_pharmacy_data():
    # Logique pour récupérer les données de la pharmacie depuis la base de données
    return "Données de la pharmacie"

# app/routes/finance_routes.py
from flask import Blueprint

finance_routes = Blueprint('finance', __name__)

@finance_routes.route('/finances', methods=['GET'])
def get_finances():
    # Logique pour récupérer les données financières depuis la base de données
    return "Données financières"

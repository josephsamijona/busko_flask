# app/routes/lab_routes.py
from flask import Blueprint

lab_routes = Blueprint('lab', __name__)

@lab_routes.route('/labs', methods=['GET'])
def get_lab_data():
    # Logique pour récupérer les données du laboratoire depuis la base de données
    return "Données du laboratoire"

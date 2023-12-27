# app/routes/patient_routes.py
from flask import Blueprint

patient_routes = Blueprint('patients', __name__)

@patient_routes.route('/patients', methods=['GET'])
def get_patients():
    # Logique pour récupérer les patients depuis la base de données
    return "Liste des patients"

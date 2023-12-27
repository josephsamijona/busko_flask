# app/routes/prescription.py
from flask import Blueprint

prescription = Blueprint('prescription', __name__)

@prescription.route('/prescriptions', methods=['GET'])
def get_prescriptions():
    # Logique pour récupérer les prescriptions depuis la base de données
    return "Liste des prescriptions"

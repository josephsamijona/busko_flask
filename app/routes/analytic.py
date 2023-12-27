# app/routes/analytic.py
from flask import Blueprint

analytic = Blueprint('analytic', __name__)

@analytic.route('/analytics', methods=['GET'])
def get_analytics():
    # Logique pour générer et récupérer des analyses
    return "Analyses"

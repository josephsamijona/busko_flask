# app/routes/rendezvous_routes.py
from flask import Blueprint

rendezvous_routes = Blueprint('rendezvous', __name__)

@rendezvous_routes.route('/rendezvous', methods=['GET'])
def get_rendezvous():
    # Logique pour récupérer les rendez-vous depuis la base de données
    return "Liste des rendez-vous"

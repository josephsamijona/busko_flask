# app/routes/histrdvous.py
from flask import Blueprint

histrdvous = Blueprint('histrdvous', __name__)

@histrdvous.route('/history-rendezvous', methods=['GET'])
def get_history_rendezvous():
    # Logique pour récupérer l'historique des rendez-vous
    return "Historique des rendez-vous"

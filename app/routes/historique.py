# app/routes/historique.py
from flask import Blueprint

historique = Blueprint('historique', __name__)

@historique.route('/history', methods=['GET'])
def get_history():
    # Logique pour récupérer l'historique global
    return "Historique global"

# app/routes/setting.py
from flask import Blueprint

setting = Blueprint('setting', __name__)

@setting.route('/settings', methods=['GET'])
def get_settings():
    # Logique pour récupérer les paramètres et configurations
    return "Paramètres et configurations"

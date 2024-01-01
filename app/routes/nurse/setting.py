# app/routes/setting.py
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Configuration

# Créez un Blueprint pour les routes des paramètres
setting_bp = Blueprint('setting', __name__)

# Route pour obtenir les paramètres actuels de l'application
@setting_bp.route('/get-settings', methods=['GET'])
@login_required
def get_settings():
    # Assurez-vous que l'utilisateur a les autorisations nécessaires
    if current_user.role not in ['admin', 'super_admin']:
        return jsonify({'message': 'Accès non autorisé'}), 403

    # Récupérez tous les paramètres depuis la base de données
    configurations = Configuration.query.all()

    # Construisez la réponse JSON
    settings = {config.key: config.value for config in configurations}

    return jsonify({'settings': settings}), 200

# Route pour mettre à jour les paramètres de l'application
@setting_bp.route('/update-settings', methods=['POST'])
@login_required
def update_settings():
    # Assurez-vous que l'utilisateur a les autorisations nécessaires
    if current_user.role not in ['admin', 'super_admin']:
        return jsonify({'message': 'Accès non autorisé'}), 403

    # Récupérez les nouvelles configurations depuis la demande de l'utilisateur
    new_settings = request.json.get('settings')

    # Mettez à jour les paramètres dans la base de données
    for key, value in new_settings.items():
        config = Configuration.query.filter_by(key=key).first()
        if config:
            config.value = value
        else:
            # Si la clé n'existe pas, créez-la
            config = Configuration(key=key, value=value)
            config.save()

    return jsonify({'message': 'Paramètres mis à jour avec succès'}), 200

# Vous pouvez ajouter d'autres routes ou ressources pour la gestion des paramètres

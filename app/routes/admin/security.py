# app/routes/admin/security.py
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Utilisateur, db
from werkzeug.security import generate_password_hash

# Créez un Blueprint pour les routes de sécurité et contrôle d'accès
security_bp = Blueprint('security', __name__, url_prefix='/admin/security')

@security_bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    data = request.get_json()

    if 'user_id' not in data or 'new_password' not in data:
        return jsonify({'message': 'Missing data'}), 400

    user_id = data['user_id']
    new_password = data['new_password']

    # Vérifiez si l'utilisateur actuel a les autorisations nécessaires
    if current_user.Account_Type != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    # Recherchez l'utilisateur dans la base de données
    user_to_update = Utilisateur.query.get(user_id)

    if user_to_update:
        # Mettez à jour le mot de passe de l'utilisateur
        user_to_update.Password = generate_password_hash(new_password, method='sha256')
        db.session.commit()

        return jsonify({'message': 'Password updated successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@security_bp.route('/check_permissions', methods=['POST'])
@login_required
def check_permissions():
    data = request.get_json()

    if 'user_id' not in data or 'required_permissions' not in data:
        return jsonify({'message': 'Missing data'}), 400

    user_id = data['user_id']
    required_permissions = data['required_permissions']

    # Appeler la fonction pour vérifier les autorisations
    result = check_permissions(user_id, required_permissions)

    return jsonify({'message': result}), 200

@security_bp.route('/check_access_rights', methods=['POST'])
@login_required
def check_access_rights():
    data = request.get_json()

    if 'user_id' not in data or 'resource_id' not in data:
        return jsonify({'message': 'Missing data'}), 400

    user_id = data['user_id']
    resource_id = data['resource_id']

    # Appeler la fonction pour vérifier les droits d'accès
    result = check_access_rights(user_id, resource_id)

    return jsonify({'message': result}), 200

@security_bp.route('/manage_sessions', methods=['POST'])
@login_required
def manage_sessions():
    data = request.get_json()

    if 'user_id' not in data or 'action' not in data:
        return jsonify({'message': 'Missing data'}), 400

    user_id = data['user_id']
    action = data['action']

    # Appeler la fonction pour gérer les sessions
    manage_sessions(user_id, action)

    return jsonify({'message': 'Session managed successfully'}), 200

@security_bp.route('/log_security_event', methods=['POST'])
@login_required
def log_security_event():
    data = request.get_json()

    if 'event_type' not in data or 'user_id' not in data or 'details' not in data:
        return jsonify({'message': 'Missing data'}), 400

    event_type = data['event_type']
    user_id = data['user_id']
    details = data['details']

    # Appeler la fonction pour enregistrer un événement de sécurité
    log_security_event(event_type, user_id, details)

    return jsonify({'message': 'Security event logged successfully'}), 200

# Ajoutez d'autres routes et fonctions de sécurité selon vos besoins

    # Vérifier les autorisations d'un utilisateur
     

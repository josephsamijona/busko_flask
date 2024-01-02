from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Utilisateur
from app.utils import send_alert_email, send_alert_sms

# Créez un Blueprint pour les routes de notifications
notif_bp = Blueprint('notif', __name__, url_prefix='/admin/notif')

@notif_bp.route('/send_signup_alert', methods=['POST'])
@login_required
def send_signup_alert():
    data = request.get_json()

    if 'user_id' not in data:
        return jsonify({'message': 'Missing data'}), 400

    user_id = data['user_id']

    # Vérifiez si l'utilisateur actuel a les autorisations nécessaires
    if current_user.Account_Type != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    # Recherchez l'utilisateur dans la base de données
    user_to_alert = Utilisateur.query.get(user_id)

    if user_to_alert:
        # Envoyez l'alerte par e-mail
        send_alert_email(subject='New User Signup', message=f"New user signed up: {user_to_alert.First_Name} {user_to_alert.Last_Name} ({user_to_alert.username})")

        # Envoyez l'alerte par SMS
        send_alert_sms(message=f"New user signed up: {user_to_alert.username}")

        return jsonify({'message': 'Signup alert sent successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@notif_bp.route('/send_login_alert', methods=['POST'])
@login_required
def send_login_alert():
    data = request.get_json()

    if 'user_id' not in data:
        return jsonify({'message': 'Missing data'}), 400

    user_id = data['user_id']

    # Vérifiez si l'utilisateur actuel a les autorisations nécessaires
    if current_user.Account_Type != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    # Recherchez l'utilisateur dans la base de données
    user_to_alert = Utilisateur.query.get(user_id)

    if user_to_alert:
        # Envoyez l'alerte par e-mail
        send_alert_email(subject='User Login Alert', message=f"User logged in: {user_to_alert.First_Name} {user_to_alert.Last_Name} ({user_to_alert.username})")

        # Envoyez l'alerte par SMS
        send_alert_sms(message=f"User logged in: {user_to_alert.username}")

        return jsonify({'message': 'Login alert sent successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@notif_bp.route('/send_logout_alert', methods=['POST'])
@login_required
def send_logout_alert():
    data = request.get_json()

    if 'user_id' not in data:
        return jsonify({'message': 'Missing data'}), 400

    user_id = data['user_id']

    # Vérifiez si l'utilisateur actuel a les autorisations nécessaires
    if current_user.Account_Type != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    # Recherchez l'utilisateur dans la base de données
    user_to_alert = Utilisateur.query.get(user_id)

    if user_to_alert:
        # Envoyez l'alerte par e-mail
        send_alert_email(subject='User Logout Alert', message=f"User logged out: {user_to_alert.First_Name} {user_to_alert.Last_Name} ({user_to_alert.username})")

        # Envoyez l'alerte par SMS
        send_alert_sms(message=f"User logged out: {user_to_alert.username}")

        return jsonify({'message': 'Logout alert sent successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404
    
    
    
@notif_bp.route('/send_password_reset_alert', methods=['POST'])
@login_required
def send_password_reset_alert():
    data = request.get_json()

    if 'user_id' not in data:
        return jsonify({'message': 'Missing data'}), 400

    user_id = data['user_id']

    # Vérifiez si l'utilisateur actuel a les autorisations nécessaires
    if current_user.Account_Type != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    # Recherchez l'utilisateur dans la base de données
    user_to_alert = Utilisateur.query.get(user_id)

    if user_to_alert:
        # Envoyez l'alerte par e-mail
        send_alert_email(subject='Password Reset Request', message=f"Password reset requested for {user_to_alert.First_Name} {user_to_alert.Last_Name} ({user_to_alert.username})")

        # Envoyez l'alerte par SMS
        send_alert_sms(message=f"Password reset requested for {user_to_alert.username}")

        return jsonify({'message': 'Password reset alert sent successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

# Ajoutez d'autres routes et fonctions de notifications selon vos besoins
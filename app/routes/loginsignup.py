# Importations nécessaires
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Utilisateur  # Assurez-vous d'importer le modèle Utilisateur
from app import mail
from random import randint
from flask_mail import Message
from twilio.rest import Client 
from app import db
import random
import string
from datetime import datetime
from app.utils import send_alert_email, send_alert_sms

# Création du Blueprint pour la gestion d'authentification
auth_bp = Blueprint('auth', __name__)

# Fonction pour gérer la connexion
@auth_bp.route('/login', methods=['POST'])
def patient_login():
    data = request.get_json()

    # Assurez-vous que les données nécessaires sont fournies
    if 'login_identifier' not in data or 'password' not in data:
        return jsonify({'message': 'Missing data'}), 400

    login_identifier = data['login_identifier']
    password = data['password']

    # Recherchez l'utilisateur dans la base de données
    user = Utilisateur.query.filter(
        (Utilisateur.username == login_identifier) |
        (Utilisateur.email == login_identifier) |
        (Utilisateur.phone == login_identifier)
    ).first()

    # Vérifiez le mot de passe
    if user and check_password_hash(user.password, password):
        # Connectez l'utilisateur
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200

    return jsonify({'message': 'Invalid login identifier or password'}), 401

# Fonction pour gérer l'inscription des patients
 
@auth_bp.route('/signup/patient', methods=['POST'])
def signup_patient():
    data = request.get_json()

    # Assurez-vous que les données nécessaires sont fournies
    if 'first_name' not in data or 'last_name' not in data or 'email' not in data or 'phone' not in data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Missing data'}), 400

    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    phone = data['phone']
    username = data['username']
    password = data['password']

    # Générez le User_Id en utilisant les deux premières lettres de First_Name, Last_Name, et un chiffre aléatoire
    user_id = first_name[:2].lower() + last_name[:2].lower() + str(random.randint(10, 99))

    # Date de création actuelle
    date_of_creation = datetime.now().date()

    # Créez un nouvel utilisateur de type "patient"
    new_user = Utilisateur(
        User_Id=user_id,
        First_Name=first_name,
        Last_Name=last_name,
        Email=email,
        Phone=phone,
        Username=username,
        Password=generate_password_hash(password, method='sha256'),
        Date_of_Creation=date_of_creation,
        Account_Type='patient'
        # Ajoutez d'autres champs si nécessaire
    )

    # Ajoutez l'utilisateur à la base de données
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Patient signup successful'}), 201

## DOCTOR LOGIN

@auth_bp.route('/login/doctor', methods=['POST'])
def login_doctor():
    data = request.get_json()

    # Assurez-vous que les données nécessaires sont fournies
    if 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Missing data'}), 400

    # Recherchez l'utilisateur dans la base de données
    doctor = Utilisateur.query.filter_by(username=data['username'], Account_Type='doctor').first()

    # Vérifiez le mot de passe
    if doctor and check_password_hash(doctor.password, data['password']):
        # Connectez le docteur
        login_user(doctor)
        return jsonify({'message': 'Doctor login successful'}), 200

    return jsonify({'message': 'Invalid username or password'}), 401


# Fonction pour gérer l'inscription des médecins
@auth_bp.route('/signup/doctor', methods=['POST'])
def signup_doctor():
    data = request.get_json()

    # Assurez-vous que les données nécessaires sont fournies
    if 'first_name' not in data or 'last_name' not in data or 'email' not in data or 'phone' not in data or 'username' not in data:
        return jsonify({'message': 'Missing data'}), 400

    # Générez le User_Id en prenant les deux premières lettres du First_Name et du Last_Name et un chiffre aléatoire
    user_id = f"{data['first_name'][:2]}{data['last_name'][:2]}{randint(10, 99)}"

    # Créez un nouvel utilisateur de type "doctor"
    new_doctor = Utilisateur(
        User_Id=user_id,
        First_Name=data['first_name'],
        Last_Name=data['last_name'],
        Email=data['email'],
        Phone=data['phone'],
        Username=data['username'],
        password=generate_password_hash(data['password'], method='sha256'),
        Account_Type='doctor',
        # Ajoutez d'autres champs si nécessaire
    )

    # Ajoutez le docteur à la base de données
    db.session.add(new_doctor)
    db.session.commit()

    return jsonify({'message': 'Doctor signup successful'}), 201

@auth_bp.route('/login/nurse', methods=['POST'])
def login_nurse():
    data = request.get_json()

    # Assurez-vous que les données nécessaires sont fournies
    if 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Missing data'}), 400

    # Recherchez l'infirmière dans la base de données
    nurse = Utilisateur.query.filter_by(username=data['username'], Account_Type='nurse').first()

    # Vérifiez le mot de passe
    if nurse and check_password_hash(nurse.password, data['password']):
        # Connectez l'infirmière
        login_user(nurse)
        return jsonify({'message': 'Login successful'}), 200

    return jsonify({'message': 'Invalid username or password'}), 401

# Fonction pour gérer l'inscription des infirmières
@auth_bp.route('/nurse-signup', methods=['POST'])
def nurse_signup():
    data = request.get_json()

    # Assurez-vous que les données nécessaires sont fournies
    required_fields = ['first_name', 'last_name', 'email', 'phone', 'username', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing data'}), 400

    # Générez le User_Id en prenant les deux premières lettres du First_Name et du Last_Name et un chiffre aléatoire
    user_id_prefix = data['first_name'][:2].lower() + data['last_name'][:2].lower()
    user_id_suffix = str(randint(100, 999))  # Utilisation de la fonction randint pour générer un chiffre aléatoire
    user_id = user_id_prefix + user_id_suffix

    # Créez un nouvel utilisateur de type 'nurse'
    new_nurse = Utilisateur(
        User_Id=user_id,
        First_Name=data['first_name'],
        Last_Name=data['last_name'],
        Email=data['email'],
        Phone=data['phone'],
        Username=data['username'],
        Password=generate_password_hash(data['password'], method='sha256'),
        Account_Type='nurse'
        # Ajoutez d'autres champs si nécessaire
    )

    # Ajoutez l'infirmière à la base de données
    db.session.add(new_nurse)
    db.session.commit()

    # Envoyez une alerte à l'administrateur
    admin_alert_message = f"Infirmière enregistrée: {new_nurse.First_Name} {new_nurse.Last_Name} ({new_nurse.username})"
    send_alert_email(subject='Alerte: Nouvelle inscription', message=admin_alert_message)
    send_alert_sms(message=admin_alert_message)

    return jsonify({'message': 'Nurse signup successful'}), 201

@auth_bp.route('/admin-login', methods=['POST'])
def admin_login():
    data = request.get_json()

    # Assurez-vous que les données nécessaires sont fournies
    if 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Missing data'}), 400

    # Recherchez l'administrateur dans la base de données
    admin = Utilisateur.query.filter_by(username=data['username'], Account_Type='admin').first()

    # Vérifiez le mot de passe
    if admin and check_password_hash(admin.password, data['password']):
        # Connectez l'administrateur
        login_user(admin)
        return jsonify({'message': 'Admin login successful'}), 200

    return jsonify({'message': 'Invalid username or password'}), 401

@auth_bp.route('/admin-signup', methods=['POST'])
@login_required
def admin_signup():
    # Assurez-vous que l'utilisateur actuel est un administrateur
    if current_user.Account_Type != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    data = request.get_json()

    # Assurez-vous que les données nécessaires sont fournies
    if 'first_name' not in data or 'last_name' not in data or 'email' not in data or 'phone' not in data or 'username' not in data:
        return jsonify({'message': 'Missing data'}), 400

    # Générez le User_Id en prenant les deux premières lettres du First_Name, du Last_Name et un chiffre aléatoire
    user_id = data['first_name'][:2].lower() + data['last_name'][:2].lower() + str(random.randint(10, 99))

    # Créez un nouvel administrateur
    new_admin = Utilisateur(
        User_Id=user_id,
        First_Name=data['first_name'],
        Last_Name=data['last_name'],
        Email=data['email'],
        Phone=data['phone'],
        Username=data['username'],
        password=generate_password_hash(data['password'], method='sha256'),
        Account_Type='admin'
        # Ajoutez d'autres champs si nécessaire
    )

    # Ajoutez l'administrateur à la base de données
    db.session.add(new_admin)
    db.session.commit()

    return jsonify({'message': 'Admin signup successful'}), 201

# Fonction pour gérer la déconnexion
@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    # Code de déconnexion existant...

# Fonction pour récupérer les informations de l'utilisateur actuellement connecté
 pass
@auth_bp.route('/user', methods=['GET'])
@login_required
def get_current_user():
    # Code pour récupérer les informations de l'utilisateur...

 # Autres fonctions pour gérer l'inscription des médecins, infirmières et admins...
 pass

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Assurez-vous que les données nécessaires sont fournies
    if 'login_identifier' not in data or 'password' not in data:
        return jsonify({'message': 'Missing data'}), 400

    login_identifier = data['login_identifier']
    password = data['password']

    # Recherchez l'utilisateur dans la base de données
    user = Utilisateur.query.filter(
        (Utilisateur.username == login_identifier) |
        (Utilisateur.email == login_identifier) |
        (Utilisateur.phone == login_identifier)
    ).first()

    # Vérifiez le mot de passe
    if user and check_password_hash(user.password, password):
        # Connectez l'utilisateur
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200

    return jsonify({'message': 'Invalid login identifier or password'}), 401


# Ajoutez une route pour la réinitialisation du mot de passe
@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()

    # Assurez-vous que les données nécessaires sont fournies
    if 'login_identifier' not in data:
        return jsonify({'message': 'Missing data'}), 400

    login_identifier = data['login_identifier']

    # Recherchez l'utilisateur dans la base de données
    user = Utilisateur.query.filter(
        (Utilisateur.email == login_identifier) |
        (Utilisateur.phone == login_identifier)
    ).first()

    if user:
        # Envoyez le lien de réinitialisation du mot de passe par e-mail ou SMS
        # Ajoutez votre logique de réinitialisation du mot de passe ici
        return jsonify({'message': 'Password reset link sent successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404
    
    
# Fonction pour réinitialiser le mot de passe de l'infirmière avec alerte à l'administrateur
@auth_bp.route('/reset-password/nurse', methods=['POST'])
def reset_password_nurse():
    data = request.get_json()

    # Assurez-vous que les données nécessaires sont fournies
    if 'username' not in data or 'new_password' not in data:
        return jsonify({'message': 'Missing data'}), 400

    # Recherchez l'infirmière dans la base de données
    nurse = Utilisateur.query.filter_by(username=data['username'], Account_Type='nurse').first()

    if nurse:
        # Réinitialisez le mot de passe
        nurse.password = generate_password_hash(data['new_password'], method='sha256')
        db.session.commit()

        # Envoyez une alerte à l'administrateur
        admin_alert_message = f"Le mot de passe de l'infirmière {nurse.First_Name} {nurse.Last_Name} ({nurse.username}) a été réinitialisé."
        send_alert_email(subject='Alerte: Réinitialisation de mot de passe', message=admin_alert_message)
        send_alert_sms(message=admin_alert_message)

        return jsonify({'message': 'Password reset successful'}), 200
    else:
        return jsonify({'message': 'Nurse not found'}), 404    
    
    
@auth_bp.route('/reset-password/doctor', methods=['POST'])
def reset_password_doctor():
    data = request.get_json()

    # Assurez-vous que les données nécessaires sont fournies
    if 'email' not in data or 'phone' not in data:
        return jsonify({'message': 'Missing data'}), 400

    # Recherchez le docteur dans la base de données
    doctor = Utilisateur.query.filter_by(email=data['email'], phone=data['phone'], Account_Type='doctor').first()

    if doctor:
        # Générez un nouveau mot de passe aléatoire
        new_password = ''.join([chr(randint(65, 90)) for _ in range(8)])

        # Mettez à jour le mot de passe dans la base de données
        doctor.password = generate_password_hash(new_password, method='sha256')
        db.session.commit()

        # Envoyez une alerte à l'administrateur
        send_admin_alert(doctor, new_password)

        return jsonify({'message': 'Password reset successful'}), 200
    else:
        return jsonify({'message': 'Invalid email or phone number for doctor'}), 400

def send_admin_alert(doctor, new_password):
    # Envoyez une alerte à l'administrateur par e-mail
    send_email_to_admin(doctor, new_password)

    # Envoyez une alerte à l'administrateur par SMS (Twilio)
    send_sms_to_admin(doctor, new_password)

    # Vous pouvez également ajouter d'autres moyens d'alerte ici

def send_email_to_admin(doctor, new_password):
    msg = Message('Password Reset Alert', sender='your_email@example.com', recipients=['admin_email@example.com'])
    msg.body = f"Dear Admin,\n\nA password reset request has been made for the doctor {doctor.username}. " \
               f"The new password is: {new_password}\n\nBest regards,\nYour App Team"
    mail.send(msg)

def send_sms_to_admin(doctor, new_password):
    # Remplacez les lignes suivantes par votre code Twilio
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Password reset for doctor {doctor.username}. New password: {new_password}",
        from_='+1234567890',  # Remplacez par votre numéro Twilio
        to='+0987654321'  # Remplacez par le numéro de l'administrateur
    )

    print(message.sid)
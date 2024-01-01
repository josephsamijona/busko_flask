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

# Fonction pour gérer l'inscription des médecins
@auth_bp.route('/doctor-signup', methods=['GET', 'POST'])
def doctor_signup():
    # Formulaire d'inscription pour les médecins
    if request.method == 'POST':
        # Traitement de la soumission du formulaire
        # ...

     return render_template('doctor_signup.html')

# Fonction pour gérer l'inscription des infirmières
@auth_bp.route('/nurse-signup', methods=['GET', 'POST'])
def nurse_signup():
    # Formulaire d'inscription pour les infirmières
    if request.method == 'POST':
        # Traitement de la soumission du formulaire
        # ...

     return render_template('nurse_signup.html')

# Fonction pour gérer l'inscription des admins
@auth_bp.route('/admin-signup', methods=['GET', 'POST'])
def admin_signup():
    # Formulaire d'inscription pour les admins
    if request.method == 'POST':
        # Traitement de la soumission du formulaire
        # ...

     return render_template('admin_signup.html')

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
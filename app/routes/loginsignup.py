# Importations nécessaires
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Utilisateur  # Assurez-vous d'importer le modèle Utilisateur
from app import db, login_manager

# Création du Blueprint pour l'authentification
auth_bp = Blueprint('auth', __name__)

# Fonction pour gérer la connexion
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Assurez-vous que les données nécessaires sont fournies
    if 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Missing data'}), 400

    # Recherchez l'utilisateur dans la base de données
    user = Utilisateur.query.filter_by(username=data['username']).first()

    # Vérifiez le mot de passe
    if user and check_password_hash(user.password, data['password']):
        # Connectez l'utilisateur
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200

    return jsonify({'message': 'Invalid username or password'}), 401

# Fonction pour gérer l'inscription
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    # Assurez-vous que les données nécessaires sont fournies
    if 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Missing data'}), 400

    # Vérifiez si l'utilisateur existe déjà
    existing_user = Utilisateur.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    # Créez un nouvel utilisateur
    new_user = Utilisateur(
        username=data['username'],
        password=generate_password_hash(data['password'], method='sha256'),
        # Ajoutez d'autres champs si nécessaire
    )

    # Ajoutez l'utilisateur à la base de données
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Signup successful'}), 201

# Fonction pour gérer la déconnexion
@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

# Fonction pour récupérer les informations de l'utilisateur actuellement connecté
@auth_bp.route('/user', methods=['GET'])
@login_required
def get_current_user():
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        # Ajoutez d'autres champs si nécessaire
    })

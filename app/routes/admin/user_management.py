# app/routes/admin/user_management.py
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Utilisateur, db
from werkzeug.security import generate_password_hash
from random import randint  

# Créez un Blueprint pour les routes de la gestion des utilisateurs
user_management_bp = Blueprint('user_management', __name__, url_prefix='/admin/user_management')

# Route pour obtenir la liste des utilisateurs
@user_management_bp.route('/get_users', methods=['GET'])
@login_required
def get_users():
    # Assurez-vous que l'utilisateur actuel est un administrateur
    if current_user.Account_Type != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    # Récupérez la liste des utilisateurs depuis la base de données
    users = Utilisateur.query.all()

    # Formattez les données pour la réponse
    user_list = [{'User_Id': user.User_Id, 'Username': user.Username, 'Email': user.Email, 'Account_Type': user.Account_Type} for user in users]

    return jsonify({'users': user_list}), 200

# Route pour attribuer un rôle à un utilisateur
@user_management_bp.route('/assign_role/<user_id>', methods=['PUT'])
@login_required
def assign_role(user_id):
    # Assurez-vous que l'utilisateur actuel est un administrateur
    if current_user.Account_Type != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    data = request.get_json()

    # Recherchez l'utilisateur dans la base de données
    user = Utilisateur.query.get(user_id)

    if user:
        # Attribuez le rôle spécifié à l'utilisateur
        if 'role' in data:
            user.Account_Type = data['role']

            # Appliquez les modifications à la base de données
            db.session.commit()

            return jsonify({'message': 'Role assigned successfully'}), 200
        else:
            return jsonify({'message': 'Role not provided'}), 400
    else:
        return jsonify({'message': 'User not found'}), 404

# Route pour gérer les autorisations d'un utilisateur
@user_management_bp.route('/manage_permissions/<user_id>', methods=['PUT'])
@login_required
def manage_permissions(user_id):
    # Assurez-vous que l'utilisateur actuel est un administrateur
    if current_user.Account_Type != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    data = request.get_json()

    # Recherchez l'utilisateur dans la base de données
    user = Utilisateur.query.get(user_id)

    if user:
        # Gérez les autorisations spécifiées pour l'utilisateur
        if 'permissions' in data:
            user.Permissions = data['permissions']

            # Appliquez les modifications à la base de données
            db.session.commit()

            return jsonify({'message': 'Permissions managed successfully'}), 200
        else:
            return jsonify({'message': 'Permissions not provided'}), 400
    else:
        return jsonify({'message': 'User not found'}), 404

# Route pour créer un nouvel utilisateur
@user_management_bp.route('/create_user', methods=['POST'])
@login_required
def create_user():
    # Assurez-vous que l'utilisateur actuel est un administrateur
    if current_user.Account_Type != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    data = request.get_json()

    # Assurez-vous que les données nécessaires sont fournies
    required_fields = ['first_name', 'last_name', 'email', 'phone', 'username', 'password', 'account_type']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing data'}), 400

    # Générez le User_Id en prenant les deux premières lettres du First_Name et du Last_Name et un chiffre aléatoire
    user_id = f"{data['first_name'][:2]}{data['last_name'][:2]}{randint(10, 99)}"

    # Créez un nouvel utilisateur avec les données fournies
    new_user = Utilisateur(
        User_Id=user_id,
        First_Name=data['first_name'],
        Last_Name=data['last_name'],
        Email=data['email'],
        Phone=data['phone'],
        Username=data['username'],
        Password=generate_password_hash(data['password'], method='sha256'),
        Account_Type=data['account_type']
        # Ajoutez d'autres champs si nécessaire
    )

    # Ajoutez l'utilisateur à la base de données
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

# Route pour modifier les informations d'un utilisateur
@user_management_bp.route('/update_user/<user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    # Assurez-vous que l'utilisateur actuel est un administrateur
    if current_user.Account_Type != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    data = request.get_json()

    # Recherchez l'utilisateur dans la base de données
    user = Utilisateur.query.get(user_id)

    if user:
        # Mettez à jour les champs spécifiés
        if 'first_name' in data:
            user.First_Name = data['first_name']
        if 'last_name' in data:
            user.Last_Name = data['last_name']
        if 'email' in data:
            user.Email = data['email']
        if 'phone' in data:
            user.Phone = data['phone']
        if 'username' in data:
            user.Username = data['username']
        if 'password' in data:
            user.Password = generate_password_hash(data['password'], method='sha256')
        if 'account_type' in data:
            user.Account_Type = data['account_type']

        # Appliquez les modifications à la base de données
        db.session.commit()

        return jsonify({'message': 'User updated successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

# Route pour supprimer un utilisateur
@user_management_bp.route('/delete_user/<user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    # Assurez-vous que l'utilisateur actuel est un administrateur
    if current_user.Account_Type != 'admin':
        return jsonify({'message': 'Permission denied'}), 403

    # Recherchez l'utilisateur dans la base de données
    user = Utilisateur.query.get(user_id)

    if user:
        # Supprimez l'utilisateur de la base de données
        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

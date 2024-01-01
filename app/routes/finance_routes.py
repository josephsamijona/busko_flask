from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from flask_login import login_required
from app.models import Depense, Revenu  # Assurez-vous d'importer les modèles nécessaires
from app import db

# Créez un Blueprint pour les routes financières
finance_bp = Blueprint('finance', __name__)
api = Api(finance_bp)

# Classe pour les opérations financières
class FinanceManagement(Resource):
    @login_required
    def get(self, finance_id):
        # Récupérez les détails spécifiques d'une transaction financière (Dépense, Revenu, etc.)
        finance_item = None
        # Utilisez une condition pour déterminer le type de transaction (Dépense, Revenu, etc.) en fonction de l'ID ou d'autres critères

        if not finance_item:
            return jsonify({'message': 'Finance item not found'}), 404

        return jsonify({
            'id': finance_item.id,
            'amount': finance_item.amount,
            'description': finance_item.description,
            # Ajoutez d'autres champs selon vos besoins
        })

    @login_required
    def post(self):
        data = request.get_json()

        # Assurez-vous que les données nécessaires sont fournies
        if 'amount' not in data:
            return jsonify({'message': 'Missing data'}), 400

        # Créez une nouvelle transaction financière (Dépense, Revenu, etc.)
        new_finance_item = Depense(
            amount=data['amount'],
            description=data.get('description', ''),
            # Ajoutez d'autres champs selon vos besoins
        )

        db.session.add(new_finance_item)
        db.session.commit()

        return jsonify({'message': 'Finance item added successfully'}), 201

    @login_required
    def put(self, finance_id):
        data = request.get_json()

        # Récupérez la transaction financière existante (Dépense, Revenu, etc.)
        finance_item = None
        # Utilisez une condition pour déterminer le type de transaction (Dépense, Revenu, etc.) en fonction de l'ID ou d'autres critères

        if not finance_item:
            return jsonify({'message': 'Finance item not found'}), 404

        # Mettez à jour les détails de la transaction financière
        finance_item.amount = data.get('amount', finance_item.amount)
        finance_item.description = data.get('description', finance_item.description)
        # Mettez à jour d'autres champs selon vos besoins

        db.session.commit()

        return jsonify({'message': 'Finance item updated successfully'}), 200

    @login_required
    def delete(self, finance_id):
        # Supprimez la transaction financière (Dépense, Revenu, etc.)
        finance_item = None
        # Utilisez une condition pour déterminer le type de transaction (Dépense, Revenu, etc.) en fonction de l'ID ou d'autres critères

        if not finance_item:
            return jsonify({'message': 'Finance item not found'}), 404

        db.session.delete(finance_item)
        db.session.commit()

        return jsonify({'message': 'Finance item deleted successfully'}), 200

# Ajoutez la ressource au chemin spécifié
api.add_resource(FinanceManagement, '/finance/<int:finance_id>')

# Vous pouvez ajouter d'autres routes ou ressources pour la gestion des finances


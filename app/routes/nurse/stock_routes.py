from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from flask_login import login_required
from app.models import ArticleInventaire  # Assurez-vous d'importer le modèle ArticleInventaire
from app import db

# Créez un Blueprint pour les routes de l'inventaire
stock_bp = Blueprint('stock', __name__)
api = Api(stock_bp)

# Classe pour les opérations sur l'inventaire
class StockManagement(Resource):
    @login_required
    def get(self, stock_id):
        # Récupérez les détails spécifiques d'un article d'inventaire
        stock_item = ArticleInventaire.query.get(stock_id)

        if not stock_item:
            return jsonify({'message': 'Stock item not found'}), 404

        return jsonify({
            'id': stock_item.id,
            'name': stock_item.name,
            'quantity': stock_item.quantity,
            'description': stock_item.description,
            # Ajoutez d'autres champs selon vos besoins
        })

    @login_required
    def post(self):
        data = request.get_json()

        # Assurez-vous que les données nécessaires sont fournies
        if 'name' not in data or 'quantity' not in data:
            return jsonify({'message': 'Missing data'}), 400

        # Créez un nouvel article d'inventaire
        new_stock_item = ArticleInventaire(
            name=data['name'],
            quantity=data['quantity'],
            description=data.get('description', '')
            # Ajoutez d'autres champs selon vos besoins
        )

        db.session.add(new_stock_item)
        db.session.commit()

        return jsonify({'message': 'Stock item added successfully'}), 201

    @login_required
    def put(self, stock_id):
        data = request.get_json()

        # Récupérez l'article d'inventaire existant
        stock_item = ArticleInventaire.query.get(stock_id)

        if not stock_item:
            return jsonify({'message': 'Stock item not found'}), 404

        # Mettez à jour les détails de l'article d'inventaire
        stock_item.name = data.get('name', stock_item.name)
        stock_item.quantity = data.get('quantity', stock_item.quantity)
        stock_item.description = data.get('description', stock_item.description)
        # Mettez à jour d'autres champs selon vos besoins

        db.session.commit()

        return jsonify({'message': 'Stock item updated successfully'}), 200

    @login_required
    def delete(self, stock_id):
        # Supprimez l'article d'inventaire
        stock_item = ArticleInventaire.query.get(stock_id)

        if not stock_item:
            return jsonify({'message': 'Stock item not found'}), 404

        db.session.delete(stock_item)
        db.session.commit()

        return jsonify({'message': 'Stock item deleted successfully'}), 200

# Ajoutez la ressource au chemin spécifié
api.add_resource(StockManagement, '/stock/<int:stock_id>')

# Vous pouvez ajouter d'autres routes ou ressources pour la gestion de l'inventaire



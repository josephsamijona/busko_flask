from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from flask_login import login_required
from app.models import Medicament  # Assurez-vous d'importer le modèle Medicament
from app import db

# Créez un Blueprint pour les routes de la pharmacie
pharmacy_bp = Blueprint('pharmacy', __name__)
api = Api(pharmacy_bp)

# Classe pour les opérations du Point de Vente (POS)
class PointOfSale(Resource):
    @login_required
    def post(self):
        data = request.get_json()

        # Assurez-vous que les données nécessaires sont fournies
        if 'medication_id' not in data or 'quantity' not in data:
            return jsonify({'message': 'Missing data'}), 400

        # Recherchez le médicament dans la base de données
        medication = Medicament.query.get(data['medication_id'])

        if not medication:
            return jsonify({'message': 'Medication not found'}), 404

        # Vérifiez si la quantité est disponible en stock
        if medication.stock_quantity < data['quantity']:
            return jsonify({'message': 'Insufficient stock'}), 400

        # Effectuez la vente (réduisez la quantité en stock)
        medication.stock_quantity -= data['quantity']
        db.session.commit()

        return jsonify({'message': 'Sale successful'}), 200

# Ajoutez la ressource au chemin spécifié
api.add_resource(PointOfSale, '/point-of-sale')

# Vous pouvez ajouter d'autres routes ou ressources pour la gestion de la pharmacie



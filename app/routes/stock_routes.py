# app/routes/stock_routes.py
from flask import Blueprint

stock_routes = Blueprint('stock', __name__)

@stock_routes.route('/stocks', methods=['GET'])
def get_stocks():
    # Logique pour récupérer les stocks depuis la base de données
    return "Liste des stocks"

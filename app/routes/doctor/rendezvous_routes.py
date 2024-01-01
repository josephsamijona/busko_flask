# Importations nécessaires
from flask import Blueprint, request, jsonify
from app.models import Rendezvous, Patient  # Assurez-vous d'importer le modèle Patient
from app import db

# Création du Blueprint pour les rendez-vous
rendezvous_bp = Blueprint('rendezvous', __name__)

# Route pour créer un rendez-vous
@rendezvous_bp.route('/create', methods=['POST'])
def create_rendezvous():
    data = request.get_json()

    # Assurez-vous que les données nécessaires sont fournies
    if 'patient_id' not in data or 'date' not in data or 'heure' not in data:
        return jsonify({'message': 'Missing data'}), 400

    # Vérifiez si le patient existe
    patient = Patient.query.get(data['patient_id'])
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404

    # Créez un nouveau rendez-vous
    new_rendezvous = Rendezvous(
        patient_id=data['patient_id'],
        date=data['date'],
        heure=data['heure']
        # Ajoutez d'autres champs si nécessaire
    )

    # Ajoutez le rendez-vous à la base de données
    db.session.add(new_rendezvous)
    db.session.commit()

    return jsonify({'message': 'Rendez-vous created successfully'}), 201

# Route pour récupérer tous les rendez-vous
@rendezvous_bp.route('/all', methods=['GET'])
def get_all_rendezvous():
    rendezvous_list = Rendezvous.query.all()
    rendezvous_data = []

    for rendezvous in rendezvous_list:
        rendezvous_data.append({
            'id': rendezvous.id,
            'patient_id': rendezvous.patient_id,
            'date': rendezvous.date,
            'heure': rendezvous.heure
            # Ajoutez d'autres champs si nécessaire
        })

    return jsonify({'rendezvous': rendezvous_data})

# Autres routes pour la mise à jour, la suppression, etc. si nécessaire


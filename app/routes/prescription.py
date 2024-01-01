# Importations nécessaires
from flask import Blueprint, request, jsonify
from app.models import Prescription, Patient  # Assurez-vous d'importer le modèle Patient
from app import db

# Création du Blueprint pour les prescriptions
prescription_bp = Blueprint('prescription', __name__)

# Route pour créer une prescription médicale
@prescription_bp.route('/create', methods=['POST'])
def create_prescription():
    data = request.get_json()

    # Assurez-vous que les données nécessaires sont fournies
    if 'patient_id' not in data or 'medicaments' not in data:
        return jsonify({'message': 'Missing data'}), 400

    # Vérifiez si le patient existe
    patient = Patient.query.get(data['patient_id'])
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404

    # Créez une nouvelle prescription médicale
    new_prescription = Prescription(
        patient_id=data['patient_id'],
        medicaments=data['medicaments'],
        posologie=data.get('posologie', ''),
        remarques=data.get('remarques', '')
        # Ajoutez d'autres champs si nécessaire
    )

    # Ajoutez la prescription à la base de données
    db.session.add(new_prescription)
    db.session.commit()

    return jsonify({'message': 'Prescription created successfully'}), 201

# Route pour récupérer toutes les prescriptions d'un patient
@prescription_bp.route('/patient/<int:patient_id>', methods=['GET'])
def get_patient_prescriptions(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404

    prescriptions = Prescription.query.filter_by(patient_id=patient_id).all()
    prescriptions_data = []

    for prescription in prescriptions:
        prescriptions_data.append({
            'id': prescription.id,
            'medicaments': prescription.medicaments,
            'posologie': prescription.posologie,
            'remarques': prescription.remarques
            # Ajoutez d'autres champs si nécessaire
        })

    return jsonify({'prescriptions': prescriptions_data})

# Autres routes pour la mise à jour, la suppression, etc. si nécessaire

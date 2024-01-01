# app/routes/patient_routes.py
# Importations nécessaires
from flask import Blueprint, request, jsonify
from app.models import Patient  # Assurez-vous d'importer le modèle Patient
from app import db

# Création du Blueprint pour les patients
patient_bp = Blueprint('patient', __name__)

# Route pour créer un nouveau patient
@patient_bp.route('/create', methods=['POST'])
def create_patient():
    data = request.get_json()

    # Assurez-vous que les données nécessaires sont fournies
    if 'nom' not in data or 'prenom' not in data or 'date_naissance' not in data:
        return jsonify({'message': 'Missing data'}), 400

    # Créez un nouveau patient
    new_patient = Patient(
        nom=data['nom'],
        prenom=data['prenom'],
        date_naissance=data['date_naissance'],
        # Ajoutez d'autres champs si nécessaire
    )

    # Ajoutez le patient à la base de données
    db.session.add(new_patient)
    db.session.commit()

    return jsonify({'message': 'Patient created successfully'}), 201

# Route pour récupérer tous les patients
@patient_bp.route('/all', methods=['GET'])
def get_all_patients():
    patients = Patient.query.all()
    patients_data = []

    for patient in patients:
        patients_data.append({
            'id': patient.id,
            'nom': patient.nom,
            'prenom': patient.prenom,
            'date_naissance': patient.date_naissance,
            # Ajoutez d'autres champs si nécessaire
        })

    return jsonify({'patients': patients_data})

# Autres routes pour la mise à jour, la suppression, etc. si nécessaire


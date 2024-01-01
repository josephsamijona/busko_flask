from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Serologie, ExamensSelles, ExamensBiochimie, ExamenUrine, ExamensHemogramme

# Créez un Blueprint pour les routes du laboratoire
lab_bp = Blueprint('lab', __name__)

# Route pour remplir les résultats des tests de laboratoire
@lab_bp.route('/remplir-resultats', methods=['POST'])
@login_required
def remplir_resultats():
    # Assurez-vous que l'utilisateur est un médecin ou un personnel de laboratoire autorisé
    if current_user.role not in ['medecin', 'personnel_laboratoire']:
        return jsonify({'message': 'Accès non autorisé'}), 403

    # Récupérez les données de la demande de l'utilisateur
    data = request.json

    # Récupérez le type d'examen
    type_examen = data.get('type_examen')

    # Récupérez l'ID du patient
    patient_id = data.get('patient_id')

    # Récupérez les résultats spécifiques à chaque type d'examen
    if type_examen == 'serologie':
        # Exemple pour la sérologie
        resultat = data.get('resultat')
        date_resultat = data.get('date_resultat')

        # Enregistrez les résultats dans la base de données
        serologie = Serologie(patient_id=patient_id, resultat=resultat, date_resultat=date_resultat)
        serologie.save()

    elif type_examen == 'selles':
        # Exemple pour les examens de selles
        # ...

    # Ajoutez d'autres cas pour les différents types d'examens

     return jsonify({'message': 'Résultats enregistrés avec succès'}), 200

# Route pour consulter les résultats des tests de laboratoire d'un patient
@lab_bp.route('/consulter-resultats/<int:patient_id>', methods=['GET'])
@login_required
def consulter_resultats(patient_id):
    # Assurez-vous que l'utilisateur est un médecin ou un personnel de laboratoire autorisé
    if current_user.role not in ['medecin', 'personnel_laboratoire']:
        return jsonify({'message': 'Accès non autorisé'}), 403

    # Récupérez les résultats des différents types d'examens pour le patient
    serologie = Serologie.query.filter_by(patient_id=patient_id).first()
    examens_selles = ExamensSelles.query.filter_by(patient_id=patient_id).first()
    examens_biochimie = ExamensBiochimie.query.filter_by(patient_id=patient_id).first()
    examens_urine = ExamenUrine.query.filter_by(patient_id=patient_id).first()
    examens_hemogramme = ExamensHemogramme.query.filter_by(patient_id=patient_id).first()

    # Construisez la réponse JSON
    resultats = {
        'serologie': serologie.to_dict() if serologie else None,
        'examens_selles': examens_selles.to_dict() if examens_selles else None,
        'examens_biochimie': examens_biochimie.to_dict() if examens_biochimie else None,
        'examens_urine': examens_urine.to_dict() if examens_urine else None,
        'examens_hemogramme': examens_hemogramme.to_dict() if examens_hemogramme else None,
    }

    return jsonify({'resultats': resultats}), 200

# Vous pouvez ajouter d'autres routes ou ressources pour le laboratoire

from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.models import Rendezvous
from datetime import datetime

# Créez un Blueprint pour les routes du tableau de bord
dashboard_bp = Blueprint('dashboard', __name__)

# Route pour obtenir les informations du tableau de bord
@dashboard_bp.route('/home', methods=['GET'])
@login_required
def home():
    # Récupérez les rendez-vous du jour
    current_date = datetime.today().date()
    current_appointments = Rendezvous.query.filter_by(date=current_date, medecin_id=current_user.id).all()

    # Construisez la liste des notifications pour le tableau de bord
    notifications = []
    for appointment in current_appointments:
        notifications.append({
            'patient_nom': appointment.patient.nom,
            'patient_prenom': appointment.patient.prenom,
            'heure_rdv': appointment.heure_rdv.strftime('%H:%M'),
            # Ajoutez d'autres champs selon vos besoins
        })

    # Vous pouvez également ajouter d'autres informations du tableau de bord
    dashboard_info = {
        'nombre_patients': len(current_appointments),
        'nombre_rdv_jour': len(current_appointments),
        # Ajoutez d'autres champs selon vos besoins
    }

    return jsonify({
        'dashboard_info': dashboard_info,
        'notifications': notifications
    }), 200

# Vous pouvez ajouter d'autres routes ou ressources pour le tableau de bord



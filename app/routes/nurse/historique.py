from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.models import HistoriqueRendezvous, HistoriqueDossiersMedicaux, Ventes, HistoriqueMedicamentsPharmacie
from datetime import datetime

# Créez un Blueprint pour les routes de l'historique
historique_bp = Blueprint('historique', __name__)

# Route pour obtenir l'historique des rendez-vous
@historique_bp.route('/rendezvous', methods=['GET'])
@login_required
def historique_rendezvous():
    # Récupérez l'historique des rendez-vous pour l'utilisateur actuel
    historique_rendezvous = HistoriqueRendezvous.query.filter_by(medecin_id=current_user.id).all()

    # Construisez la réponse JSON
    rendezvous_data = []
    for rendezvous in historique_rendezvous:
        rendezvous_data.append({
            'patient_nom': rendezvous.patient.nom,
            'patient_prenom': rendezvous.patient.prenom,
            'date': rendezvous.date.strftime('%Y-%m-%d'),
            'heure_rdv': rendezvous.heure_rdv.strftime('%H:%M'),
            # Ajoutez d'autres champs selon vos besoins
        })

    return jsonify({'historique_rendezvous': rendezvous_data}), 200

# Route pour obtenir l'historique des fiches de prescription
@historique_bp.route('/fiches-prescription', methods=['GET'])
@login_required
def historique_fiches_prescription():
    # Récupérez l'historique des fiches de prescription pour l'utilisateur actuel
    historique_fiches_prescription = HistoriqueDossiersMedicaux.query.filter_by(medecin_id=current_user.id).all()

    # Construisez la réponse JSON
    fiches_prescription_data = []
    for fiche_prescription in historique_fiches_prescription:
        fiches_prescription_data.append({
            'patient_nom': fiche_prescription.patient.nom,
            'patient_prenom': fiche_prescription.patient.prenom,
            'date': fiche_prescription.date.strftime('%Y-%m-%d'),
            # Ajoutez d'autres champs selon vos besoins
        })

    return jsonify({'historique_fiches_prescription': fiches_prescription_data}), 200

# Route pour obtenir l'historique des achats de la pharmacie
@historique_bp.route('/achats-pharmacie', methods=['GET'])
@login_required
def historique_achats_pharmacie():
    # Récupérez l'historique des achats de la pharmacie pour l'utilisateur actuel
    historique_achats_pharmacie = HistoriqueMedicamentsPharmacie.query.filter_by(pharmacien_id=current_user.id).all()

    # Construisez la réponse JSON
    achats_pharmacie_data = []
    for achat_pharmacie in historique_achats_pharmacie:
        achats_pharmacie_data.append({
            'medicament_nom': achat_pharmacie.medicament.nom,
            'quantite': achat_pharmacie.quantite,
            'date_achat': achat_pharmacie.date_achat.strftime('%Y-%m-%d'),
            # Ajoutez d'autres champs selon vos besoins
        })

    return jsonify({'historique_achats_pharmacie': achats_pharmacie_data}), 200

# Vous pouvez ajouter d'autres routes ou ressources pour l'historique


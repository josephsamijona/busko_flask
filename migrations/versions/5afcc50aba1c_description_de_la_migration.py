"""description_de_la_migration

Revision ID: 5afcc50aba1c
Revises: 
Create Date: 2023-12-28 11:27:30.607487

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5afcc50aba1c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alertes_reapprovisionnement',
    sa.Column('Alerte_Id', sa.String(length=255), nullable=False),
    sa.Column('Article_Id', sa.String(length=255), nullable=True),
    sa.Column('Quantite_Minimale_Souhaitee', sa.Integer(), nullable=True),
    sa.Column('Quantite_Actuelle_Stock', sa.Integer(), nullable=True),
    sa.Column('Date_Alerte', sa.Date(), nullable=True),
    sa.Column('Statut_Alerte', sa.String(length=50), nullable=True),
    sa.Column('Numero_Lot_Medicament', sa.String(length=255), nullable=True),
    sa.Column('Fournisseur_Id', sa.String(length=255), nullable=True),
    sa.Column('Medicament_Commander', sa.String(length=255), nullable=True),
    sa.Column('Quantite_Commander', sa.Integer(), nullable=True),
    sa.Column('Date_Commande', sa.Date(), nullable=True),
    sa.Column('User_Id', sa.String(length=255), nullable=True),
    sa.Column('Remarques_Alerte', sa.Text(), nullable=True),
    sa.Column('Statut_Traitement_Commande', sa.String(length=50), nullable=True),
    sa.Column('Date_Reception_Medicaments', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('Alerte_Id')
    )
    op.create_table('alertes_reapprovisionnement_pharmacie',
    sa.Column('Alerte_Id', sa.String(length=255), nullable=False),
    sa.Column('Article_Id', sa.String(length=255), nullable=True),
    sa.Column('Quantite_Minimale_Souhaitee', sa.Integer(), nullable=True),
    sa.Column('Quantite_Actuelle_Stock', sa.Integer(), nullable=True),
    sa.Column('Date_Alerte', sa.Date(), nullable=True),
    sa.Column('Statut_Alerte', sa.Text(), nullable=True),
    sa.Column('Pharmacie_Id', sa.String(length=255), nullable=True),
    sa.Column('Numero_Lot_Medicament', sa.Text(), nullable=True),
    sa.Column('Reference_Fournisseur', sa.Text(), nullable=True),
    sa.Column('Medicament_Commander', sa.Text(), nullable=True),
    sa.Column('Quantite_Commander', sa.Integer(), nullable=True),
    sa.Column('Date_Commande', sa.Date(), nullable=True),
    sa.Column('User_Id', sa.String(length=255), nullable=True),
    sa.Column('Remarques_Alerte', sa.Text(), nullable=True),
    sa.Column('Statut_Traitement_Commande', sa.Text(), nullable=True),
    sa.Column('Date_Reception_Medicaments', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('Alerte_Id')
    )
    op.create_table('connexion',
    sa.Column('Connexion_Id', sa.String(length=255), nullable=False),
    sa.Column('User_Id', sa.String(length=255), nullable=True),
    sa.Column('Date_Time', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('Connexion_Id')
    )
    op.create_table('depenses',
    sa.Column('Depense_Id', sa.String(length=255), nullable=False),
    sa.Column('Categorie_Depense', sa.String(length=50), nullable=True),
    sa.Column('Date_Depense', sa.Date(), nullable=True),
    sa.Column('Montant_Depense', sa.Float(), nullable=True),
    sa.Column('Description_Depense', sa.Text(), nullable=True),
    sa.Column('Numero_Facture_Reçu', sa.String(length=255), nullable=True),
    sa.Column('Methode_Paiement', sa.String(length=50), nullable=True),
    sa.Column('Responsable_Depense', sa.String(length=255), nullable=True),
    sa.Column('Devise', sa.String(length=50), nullable=True),
    sa.Column('Taxes', sa.Float(), nullable=True),
    sa.Column('Remises', sa.Float(), nullable=True),
    sa.Column('Lieu_Depense', sa.String(length=255), nullable=True),
    sa.Column('Fournisseur_ID', sa.String(length=255), nullable=True),
    sa.Column('Numero_Bon_Commande', sa.String(length=255), nullable=True),
    sa.Column('Statut_Depense', sa.String(length=50), nullable=True),
    sa.Column('Notes_Commentaires', sa.Text(), nullable=True),
    sa.Column('Rapprochement_Comptable', sa.String(length=255), nullable=True),
    sa.Column('Type_Depense', sa.String(length=50), nullable=True),
    sa.Column('Date_Saisie', sa.DateTime(), nullable=True),
    sa.Column('Nom_Fournisseur', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('Depense_Id')
    )
    op.create_table('dossier_medical',
    sa.Column('Patient_Id', sa.String(length=255), nullable=False),
    sa.Column('Date_Ouverture_Dossier', sa.Date(), nullable=True),
    sa.Column('Nom', sa.String(length=255), nullable=True),
    sa.Column('Prenom', sa.String(length=255), nullable=True),
    sa.Column('Date_Naissance', sa.Date(), nullable=True),
    sa.Column('Genre', sa.String(length=50), nullable=True),
    sa.Column('Statut_Marital', sa.String(length=50), nullable=True),
    sa.Column('Email', sa.String(length=255), nullable=True),
    sa.Column('Telephone', sa.String(length=20), nullable=True),
    sa.Column('Telephone2', sa.String(length=20), nullable=True),
    sa.Column('Adresse', sa.String(length=255), nullable=True),
    sa.Column('Religion', sa.String(length=50), nullable=True),
    sa.Column('Nationalite', sa.String(length=50), nullable=True),
    sa.Column('Groupe_Sanguin', sa.String(length=10), nullable=True),
    sa.Column('Hauteur', sa.Float(), nullable=True),
    sa.Column('Poids', sa.Float(), nullable=True),
    sa.Column('Methode_Paiement', sa.String(length=50), nullable=True),
    sa.Column('Tension_Arterielle', sa.Float(), nullable=True),
    sa.Column('Rythme_Cardiaque', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('Patient_Id')
    )
    op.create_table('examen_urine',
    sa.Column('Examen_Id', sa.String(length=255), nullable=False),
    sa.Column('User_Id', sa.String(length=255), nullable=True),
    sa.Column('Nom', sa.String(length=255), nullable=True),
    sa.Column('Prenom', sa.String(length=255), nullable=True),
    sa.Column('Adresse', sa.String(length=255), nullable=True),
    sa.Column('Patient_Id', sa.String(length=255), nullable=True),
    sa.Column('Couleur', sa.String(length=255), nullable=True),
    sa.Column('Telephone', sa.String(length=20), nullable=True),
    sa.Column('Aspect', sa.String(length=255), nullable=True),
    sa.Column('Densite', sa.Float(), nullable=True),
    sa.Column('pH', sa.Float(), nullable=True),
    sa.Column('Glucose', sa.String(length=255), nullable=True),
    sa.Column('Proteinurie', sa.String(length=255), nullable=True),
    sa.Column('Cetone', sa.String(length=255), nullable=True),
    sa.Column('Bilirubinurie', sa.String(length=255), nullable=True),
    sa.Column('Nitrites', sa.String(length=255), nullable=True),
    sa.Column('Urobilinogene', sa.String(length=255), nullable=True),
    sa.Column('Microscopie', sa.String(length=255), nullable=True),
    sa.Column('Leucocytes', sa.String(length=255), nullable=True),
    sa.Column('Hematies', sa.String(length=255), nullable=True),
    sa.Column('CellulesEpitheliales', sa.String(length=255), nullable=True),
    sa.Column('Bacteries', sa.String(length=255), nullable=True),
    sa.Column('LevuresSimples', sa.String(length=255), nullable=True),
    sa.Column('LevuresBourgeonnantes', sa.String(length=255), nullable=True),
    sa.Column('CristauxOxalateCalcium', sa.String(length=255), nullable=True),
    sa.Column('CylindresLeucocytaires', sa.String(length=255), nullable=True),
    sa.Column('CylindresGranuleux', sa.String(length=255), nullable=True),
    sa.Column('TrichomonasVaginalis', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('Examen_Id')
    )
    op.create_table('examens_biochimie',
    sa.Column('Examen_Id', sa.String(length=255), nullable=False),
    sa.Column('Nom', sa.String(length=255), nullable=True),
    sa.Column('Prenom', sa.String(length=255), nullable=True),
    sa.Column('Adresse', sa.String(length=255), nullable=True),
    sa.Column('Patient_Id', sa.String(length=255), nullable=True),
    sa.Column('Date_Test', sa.Date(), nullable=True),
    sa.Column('User_Id', sa.String(length=255), nullable=True),
    sa.Column('Telephone', sa.String(length=20), nullable=True),
    sa.Column('Glycemie', sa.Text(), nullable=True),
    sa.Column('Azote_Uree', sa.Text(), nullable=True),
    sa.Column('Uree', sa.Text(), nullable=True),
    sa.Column('Creatinine', sa.Text(), nullable=True),
    sa.Column('BUN_Creatinine', sa.Text(), nullable=True),
    sa.Column('Proteines_Totales', sa.Text(), nullable=True),
    sa.Column('Albumine', sa.Text(), nullable=True),
    sa.Column('Globuline', sa.Text(), nullable=True),
    sa.Column('Rapport_Albumine_Globuline', sa.Text(), nullable=True),
    sa.Column('Acide_Urique', sa.Text(), nullable=True),
    sa.Column('Sodium', sa.Text(), nullable=True),
    sa.Column('Potassium', sa.Text(), nullable=True),
    sa.Column('Calcium', sa.Text(), nullable=True),
    sa.Column('CO2', sa.Text(), nullable=True),
    sa.Column('Magnesium', sa.Text(), nullable=True),
    sa.Column('Chlorure', sa.Text(), nullable=True),
    sa.Column('Bilirubine_Totale', sa.Text(), nullable=True),
    sa.Column('Bilirubine_Directe', sa.Text(), nullable=True),
    sa.Column('Bilirubine_Indirecte', sa.Text(), nullable=True),
    sa.Column('SGOT', sa.Text(), nullable=True),
    sa.Column('SGPT', sa.Text(), nullable=True),
    sa.Column('Phosphore', sa.Text(), nullable=True),
    sa.Column('Cholesterol', sa.Text(), nullable=True),
    sa.Column('HDL_Cholesterol', sa.Text(), nullable=True),
    sa.Column('Triglycerides', sa.Text(), nullable=True),
    sa.Column('VLDL_Cholesterol', sa.Text(), nullable=True),
    sa.Column('LDL_Cholesterol', sa.Text(), nullable=True),
    sa.Column('Phosphatase_Alcaline', sa.Text(), nullable=True),
    sa.Column('Prolactine', sa.Text(), nullable=True),
    sa.Column('Insuline', sa.Text(), nullable=True),
    sa.Column('Hemoglobine_Glyquee', sa.Text(), nullable=True),
    sa.Column('Fer_Serique', sa.Text(), nullable=True),
    sa.Column('Ferritine', sa.Text(), nullable=True),
    sa.Column('TLBC', sa.Text(), nullable=True),
    sa.Column('FSH_LH', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('Examen_Id')
    )
    op.create_table('examens_hemogramme',
    sa.Column('Examen_Id', sa.String(length=255), nullable=False),
    sa.Column('Nom', sa.String(length=255), nullable=True),
    sa.Column('Prenom', sa.String(length=255), nullable=True),
    sa.Column('Adresse', sa.String(length=255), nullable=True),
    sa.Column('Patient_Id', sa.String(length=255), nullable=True),
    sa.Column('Date_Test', sa.Date(), nullable=True),
    sa.Column('User_Id', sa.String(length=255), nullable=True),
    sa.Column('Telephone', sa.String(length=20), nullable=True),
    sa.Column('Globules_Rouges', sa.Text(), nullable=True),
    sa.Column('Globules_Blancs', sa.Text(), nullable=True),
    sa.Column('Hematocrite', sa.Text(), nullable=True),
    sa.Column('Hemoglobine', sa.Text(), nullable=True),
    sa.Column('MCV', sa.Text(), nullable=True),
    sa.Column('MCH', sa.Text(), nullable=True),
    sa.Column('MCHC', sa.Text(), nullable=True),
    sa.Column('Polynucleaires', sa.Text(), nullable=True),
    sa.Column('Lymphocytes', sa.Text(), nullable=True),
    sa.Column('Monocytes', sa.Text(), nullable=True),
    sa.Column('Eosinophiles', sa.Text(), nullable=True),
    sa.Column('Basophiles', sa.Text(), nullable=True),
    sa.Column('Reticulocytes', sa.Text(), nullable=True),
    sa.Column('Plaquettes', sa.Text(), nullable=True),
    sa.Column('Groupe_Sanguin', sa.Text(), nullable=True),
    sa.Column('Test_Malaria', sa.Text(), nullable=True),
    sa.Column('Test_Falciformation', sa.Text(), nullable=True),
    sa.Column('Electrophorese_Hemoglobine', sa.Text(), nullable=True),
    sa.Column('Phenotype_Groupe_Sanguin', sa.Text(), nullable=True),
    sa.Column('Vitesse_Sedimentation', sa.Text(), nullable=True),
    sa.Column('Temps_Saignement', sa.Text(), nullable=True),
    sa.Column('Temps_Coagulation', sa.Text(), nullable=True),
    sa.Column('PT', sa.Text(), nullable=True),
    sa.Column('PTT', sa.Text(), nullable=True),
    sa.Column('IRN', sa.Text(), nullable=True),
    sa.Column('D_Dimeres', sa.Text(), nullable=True),
    sa.Column('Fibrinogene', sa.Text(), nullable=True),
    sa.Column('Troponine', sa.Text(), nullable=True),
    sa.Column('CRP', sa.Text(), nullable=True),
    sa.Column('Procalcitonine', sa.Text(), nullable=True),
    sa.Column('Bilirubine_Totale', sa.Text(), nullable=True),
    sa.Column('Bilirubine_Directe', sa.Text(), nullable=True),
    sa.Column('Bilirubine_Indirecte', sa.Text(), nullable=True),
    sa.Column('Lipides_Sanguins', sa.Text(), nullable=True),
    sa.Column('Electrolytes', sa.Text(), nullable=True),
    sa.Column('Marqueurs_Hormonaux', sa.Text(), nullable=True),
    sa.Column('Tests_Allergies', sa.Text(), nullable=True),
    sa.Column('Tests_Fonction_Renale', sa.Text(), nullable=True),
    sa.Column('Tests_Coagulation', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('Examen_Id')
    )
    op.create_table('examens_selles',
    sa.Column('Examen_Id', sa.String(length=255), nullable=False),
    sa.Column('Nom', sa.String(length=255), nullable=True),
    sa.Column('Prenom', sa.String(length=255), nullable=True),
    sa.Column('Adresse', sa.String(length=255), nullable=True),
    sa.Column('Patient_Id', sa.String(length=255), nullable=True),
    sa.Column('Date_Test', sa.Date(), nullable=True),
    sa.Column('User_Id', sa.String(length=255), nullable=True),
    sa.Column('Telephone', sa.String(length=20), nullable=True),
    sa.Column('Apparence_Selles', sa.Text(), nullable=True),
    sa.Column('Consistance_Selles', sa.Text(), nullable=True),
    sa.Column('Sang_Occulte', sa.Text(), nullable=True),
    sa.Column('Oeufs_Parasites', sa.Text(), nullable=True),
    sa.Column('Bleu_Methylene', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('Examen_Id')
    )
    op.create_table('factures',
    sa.Column('Facture_Id', sa.String(length=255), nullable=False),
    sa.Column('User_Id', sa.String(length=255), nullable=True),
    sa.Column('Patient_Id', sa.String(length=255), nullable=True),
    sa.Column('Nom', sa.String(length=255), nullable=True),
    sa.Column('Prenom', sa.String(length=255), nullable=True),
    sa.Column('Adresse', sa.String(length=255), nullable=True),
    sa.Column('Date_Facture', sa.Date(), nullable=True),
    sa.Column('Montant_Total', sa.Float(), nullable=True),
    sa.Column('Statut_Facture', sa.String(length=50), nullable=True),
    sa.Column('Date_Paiement', sa.Date(), nullable=True),
    sa.Column('Methode_Paiement', sa.String(length=50), nullable=True),
    sa.Column('Description_Services_Produits', sa.Text(), nullable=True),
    sa.Column('Numero_Facture', sa.String(length=255), nullable=True),
    sa.Column('Coordonnees_Clinique', sa.Text(), nullable=True),
    sa.Column('Taxes', sa.Float(), nullable=True),
    sa.Column('Remises', sa.Float(), nullable=True),
    sa.Column('Details_Assurance', sa.Text(), nullable=True),
    sa.Column('Numero_Reference_Paiement', sa.String(length=255), nullable=True),
    sa.Column('Notes_Commentaires', sa.Text(), nullable=True),
    sa.Column('Type_Service_Produit', sa.String(length=50), nullable=True),
    sa.Column('Modes_Paiement_Acceptes', sa.Text(), nullable=True),
    sa.Column('Documents_Attaches', sa.LargeBinary(), nullable=True),
    sa.Column('Statut_Remboursement', sa.String(length=50), nullable=True),
    sa.Column('Responsable_Facturation', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('Facture_Id')
    )
    op.create_table('fiches_prescription',
    sa.Column('Fiche_Prescription_Id', sa.String(length=255), nullable=False),
    sa.Column('Patient_Id', sa.String(length=255), nullable=True),
    sa.Column('User_Id', sa.String(length=255), nullable=True),
    sa.Column('Date_Prescription', sa.Text(), nullable=True),
    sa.Column('Medicament_Prescrit', sa.Text(), nullable=True),
    sa.Column('Quantite_Prescrite', sa.Integer(), nullable=True),
    sa.Column('Frequence_Prise', sa.Text(), nullable=True),
    sa.Column('Instructions_Speciales', sa.Text(), nullable=True),
    sa.Column('Statut_Prescription', sa.Text(), nullable=True),
    sa.Column('Numero_Lot', sa.Text(), nullable=True),
    sa.Column('Date_Debut_Traitement', sa.Text(), nullable=True),
    sa.Column('Date_Fin_Traitement', sa.Text(), nullable=True),
    sa.Column('Renouvellement_Prescription', sa.Text(), nullable=True),
    sa.Column('Notes_Medecin', sa.Text(), nullable=True),
    sa.Column('Statut_Validation', sa.Text(), nullable=True),
    sa.Column('Rappels_Prescription', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('Fiche_Prescription_Id')
    )
    op.create_table('fournisseurs',
    sa.Column('Fournisseur_Id', sa.String(length=255), nullable=False),
    sa.Column('Nom_Fournisseur', sa.String(length=255), nullable=True),
    sa.Column('Adresse', sa.Text(), nullable=True),
    sa.Column('Numero_Telephone', sa.String(length=20), nullable=True),
    sa.Column('Adresse_Email', sa.String(length=255), nullable=True),
    sa.Column('Produits_Fournis', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('Fournisseur_Id')
    )
    op.create_table('historique_dossiers_medicaux',
    sa.Column('Historique_Dossiers_Medicaux_Id', sa.String(length=255), nullable=False),
    sa.Column('Patient_Id', sa.String(length=255), nullable=True),
    sa.Column('Date_Heure_Modification', sa.DateTime(), nullable=True),
    sa.Column('User_Id', sa.String(length=255), nullable=True),
    sa.Column('Champ_Modifie', sa.Text(), nullable=True),
    sa.Column('Valeur_Avant_Modification', sa.Text(), nullable=True),
    sa.Column('Nouvelle_Valeur', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('Historique_Dossiers_Medicaux_Id')
    )
    op.create_table('historique_factures',
    sa.Column('Historique_Factures_Id', sa.String(length=255), nullable=False),
    sa.Column('Facture_Id', sa.String(length=255), nullable=True),
    sa.Column('Date_Heure_Modification', sa.DateTime(), nullable=True),
    sa.Column('User_Id', sa.String(length=255), nullable=True),
    sa.Column('Montant_Modifie', sa.Float(), nullable=True),
    sa.Column('Motif_Modification', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('Historique_Factures_Id')
    )
    op.create_table('historique_medicaments_pharmacie',
    sa.Column('Historique_Medicaments_Pharmacie_Id', sa.String(length=255), nullable=False),
    sa.Column('Article_Id', sa.String(length=255), nullable=True),
    sa.Column('Date_Heure_Modification', sa.DateTime(), nullable=True),
    sa.Column('User_Id', sa.String(length=255), nullable=True),
    sa.Column('Champ_Modifie', sa.Text(), nullable=True),
    sa.Column('Valeur_Avant_Modification', sa.Text(), nullable=True),
    sa.Column('Nouvelle_Valeur', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('Historique_Medicaments_Pharmacie_Id')
    )
    op.create_table('historique_patient',
    sa.Column('Historique_Patient_Id', sa.Integer(), nullable=False),
    sa.Column('Patient_Id', sa.String(length=255), nullable=True),
    sa.Column('Date_Heure_Modification', sa.Date(), nullable=True),
    sa.Column('User_Id', sa.String(length=255), nullable=True),
    sa.Column('Champ_Modifie', sa.String(length=255), nullable=True),
    sa.Column('Valeur_Avant_Modification', sa.String(length=255), nullable=True),
    sa.Column('Nouvelle_Valeur', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('Historique_Patient_Id')
    )
    op.create_table('historique_rendezvous',
    sa.Column('Historique_Rendezvous_Id', sa.String(length=255), nullable=False),
    sa.Column('Rendezvous_Id', sa.String(length=255), nullable=True),
    sa.Column('Date_Heure_Modification', sa.DateTime(), nullable=True),
    sa.Column('User_Id', sa.String(length=255), nullable=True),
    sa.Column('Nouvelle_Date_Heure_Rendezvous', sa.DateTime(), nullable=True),
    sa.Column('Motif_Modification', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('Historique_Rendezvous_Id')
    )
    op.create_table('inventaire',
    sa.Column('Article_Id', sa.String(length=255), nullable=False),
    sa.Column('Nom_Article', sa.String(length=255), nullable=True),
    sa.Column('Description_Article', sa.Text(), nullable=True),
    sa.Column('Categorie_Id', sa.String(length=255), nullable=True),
    sa.Column('Quantite_Stock', sa.Integer(), nullable=True),
    sa.Column('Quantite_Minimale_Souhaitee', sa.Integer(), nullable=True),
    sa.Column('Prix_Unitaire', sa.Float(), nullable=True),
    sa.Column('Date_Expiration', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('Article_Id')
    )
    op.create_table('mouvements_inventaire',
    sa.Column('Mouvement_Id', sa.Integer(), nullable=False),
    sa.Column('Article_Id', sa.String(length=255), nullable=True),
    sa.Column('Type_Mouvement', sa.String(length=255), nullable=True),
    sa.Column('Date_Heure_Mouvement', sa.DateTime(), nullable=True),
    sa.Column('Quantite_Impliquee', sa.Integer(), nullable=True),
    sa.Column('User_Id', sa.String(length=255), nullable=True),
    sa.Column('Raison_Mouvement', sa.Text(), nullable=True),
    sa.Column('Nouvelle_Quantite_Stock', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('Mouvement_Id')
    )
    op.create_table('mouvements_medicaments',
    sa.Column('Mouvement_Id', sa.String(length=255), nullable=False),
    sa.Column('Article_Id', sa.String(length=255), nullable=True),
    sa.Column('Type_Mouvement', sa.Text(), nullable=True),
    sa.Column('Date_Heure_Mouvement', sa.DateTime(), nullable=True),
    sa.Column('Quantite_Impliquee', sa.Integer(), nullable=True),
    sa.Column('User_Id', sa.String(length=255), nullable=True),
    sa.Column('Raison_Mouvement', sa.Text(), nullable=True),
    sa.Column('Nouvelle_Quantite_Stock', sa.Integer(), nullable=True),
    sa.Column('Numero_Lot_Medicament', sa.Text(), nullable=True),
    sa.Column('Reference_Commande', sa.Text(), nullable=True),
    sa.Column('Cout_Unitaire', sa.Float(), nullable=True),
    sa.Column('Cout_Total', sa.Float(), nullable=True),
    sa.Column('Stock_Minimum', sa.Integer(), nullable=True),
    sa.Column('Statut_Validation', sa.Text(), nullable=True),
    sa.Column('Fournisseur_Id', sa.String(length=255), nullable=True),
    sa.Column('Commande_Client_Id', sa.Text(), nullable=True),
    sa.Column('Reference_Patient', sa.Text(), nullable=True),
    sa.Column('Emplacement_Stockage', sa.Text(), nullable=True),
    sa.Column('Methode_Stockage', sa.Text(), nullable=True),
    sa.Column('Date_Expiration_Medicament', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('Mouvement_Id')
    )
    op.create_table('rendezvous',
    sa.Column('Rendezvous_Id', sa.String(length=255), nullable=False),
    sa.Column('Nom', sa.String(length=255), nullable=True),
    sa.Column('Prenom', sa.String(length=255), nullable=True),
    sa.Column('Patient_Id', sa.String(length=255), nullable=True),
    sa.Column('Date_Heure_Rendezvous', sa.DateTime(), nullable=True),
    sa.Column('Duree_Rendezvous', sa.Integer(), nullable=True),
    sa.Column('Motif_Rendezvous', sa.Text(), nullable=True),
    sa.Column('User_Id', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('Rendezvous_Id')
    )
    op.create_table('revenus',
    sa.Column('Revenu_Id', sa.Integer(), nullable=False),
    sa.Column('Source_Revenu', sa.String(length=255), nullable=True),
    sa.Column('Date_Revenu', sa.Date(), nullable=True),
    sa.Column('Montant_Revenu', sa.Float(), nullable=True),
    sa.Column('Type_Paiement', sa.String(length=50), nullable=True),
    sa.Column('Reference_Facture', sa.String(length=255), nullable=True),
    sa.Column('Responsable_Paiement', sa.String(length=255), nullable=True),
    sa.Column('Details_Transaction', sa.Text(), nullable=True),
    sa.Column('Statut_Transaction', sa.String(length=50), nullable=True),
    sa.Column('Reference_Patient', sa.String(length=255), nullable=True),
    sa.Column('Mode_Facturation', sa.String(length=50), nullable=True),
    sa.Column('Categorie_Revenu', sa.String(length=50), nullable=True),
    sa.Column('Date_Saisie', sa.DateTime(), nullable=True),
    sa.Column('Reference_Compte_Bancaire', sa.String(length=255), nullable=True),
    sa.Column('Methode_Facturation', sa.String(length=50), nullable=True),
    sa.Column('Heure_Transaction', sa.Time(), nullable=True),
    sa.Column('Devise', sa.String(length=50), nullable=True),
    sa.Column('Taxes', sa.Float(), nullable=True),
    sa.Column('Remises', sa.Float(), nullable=True),
    sa.Column('Rapprochement_Bancaire', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('Revenu_Id')
    )
    op.create_table('serologie',
    sa.Column('Examen_Id', sa.String(length=255), nullable=False),
    sa.Column('Patient_Id', sa.String(length=255), nullable=True),
    sa.Column('Date_Examen', sa.Date(), nullable=True),
    sa.Column('User_Id', sa.String(length=255), nullable=True),
    sa.Column('Nom', sa.String(length=255), nullable=True),
    sa.Column('Prenom', sa.String(length=255), nullable=True),
    sa.Column('Adresse', sa.String(length=255), nullable=True),
    sa.Column('Telephone', sa.String(length=20), nullable=True),
    sa.Column('BHCG', sa.Text(), nullable=True),
    sa.Column('RPR', sa.Text(), nullable=True),
    sa.Column('HIV', sa.Text(), nullable=True),
    sa.Column('CRP', sa.Text(), nullable=True),
    sa.Column('ASO', sa.Text(), nullable=True),
    sa.Column('PSA', sa.Text(), nullable=True),
    sa.Column('Salmonella_O', sa.Text(), nullable=True),
    sa.Column('Salmonella_H', sa.Text(), nullable=True),
    sa.Column('H_Pyloric', sa.Text(), nullable=True),
    sa.Column('Toxoplasma_IGG', sa.Text(), nullable=True),
    sa.Column('Toxoplasma_IGM', sa.Text(), nullable=True),
    sa.Column('Rubella_IGM', sa.Text(), nullable=True),
    sa.Column('TPHA', sa.Text(), nullable=True),
    sa.Column('Chlamydia_ICG', sa.Text(), nullable=True),
    sa.Column('Chlamydia_IGM', sa.Text(), nullable=True),
    sa.Column('Facteur_Rhumatoide', sa.Text(), nullable=True),
    sa.Column('Mantoux_Test', sa.Text(), nullable=True),
    sa.Column('Herpes_Type_I_IGG', sa.Text(), nullable=True),
    sa.Column('Herpes_Type_II_IGG', sa.Text(), nullable=True),
    sa.Column('Herpes_Type_II_IGM', sa.Text(), nullable=True),
    sa.Column('Hbs_Ag', sa.Text(), nullable=True),
    sa.Column('Hepatite_C', sa.Text(), nullable=True),
    sa.Column('Mono_Test', sa.Text(), nullable=True),
    sa.Column('Virus_Hepatite_B', sa.Text(), nullable=True),
    sa.Column('Virus_Hepatite_C', sa.Text(), nullable=True),
    sa.Column('Anticorps_VIH', sa.Text(), nullable=True),
    sa.Column('Virus_Dengue', sa.Text(), nullable=True),
    sa.Column('Virus_Zika', sa.Text(), nullable=True),
    sa.Column('Virus_Fievre_Jaune', sa.Text(), nullable=True),
    sa.Column('Virus_Rubeole', sa.Text(), nullable=True),
    sa.Column('Anticorps_Toxoplasme', sa.Text(), nullable=True),
    sa.Column('Virus_Grippe', sa.Text(), nullable=True),
    sa.Column('Virus_Rougeole', sa.Text(), nullable=True),
    sa.Column('Virus_Oreillons', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('Examen_Id')
    )
    op.create_table('utilisateur',
    sa.Column('User_Id', sa.String(length=255), nullable=False),
    sa.Column('First_Name', sa.String(length=255), nullable=True),
    sa.Column('Last_Name', sa.String(length=255), nullable=True),
    sa.Column('Username', sa.String(length=255), nullable=True),
    sa.Column('Email', sa.String(length=255), nullable=True),
    sa.Column('Phone', sa.String(length=20), nullable=True),
    sa.Column('Password', sa.String(length=255), nullable=True),
    sa.Column('Date_of_Creation', sa.Date(), nullable=True),
    sa.Column('Account_Type', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('User_Id')
    )
    op.create_table('ventes',
    sa.Column('Vente_Id', sa.String(length=255), nullable=False),
    sa.Column('Article_Id', sa.String(length=255), nullable=True),
    sa.Column('Patient_Id', sa.String(length=255), nullable=True),
    sa.Column('User_Id', sa.String(length=255), nullable=True),
    sa.Column('Date_Vente', sa.Text(), nullable=True),
    sa.Column('Quantite_Vendue', sa.Integer(), nullable=True),
    sa.Column('Prix_Unitaire_Vente', sa.Float(), nullable=True),
    sa.Column('Montant_Total_Vente', sa.Float(), nullable=True),
    sa.Column('Numero_Lot_Medicament', sa.Text(), nullable=True),
    sa.Column('Heure_Vente', sa.Text(), nullable=True),
    sa.Column('Mode_Paiement', sa.Text(), nullable=True),
    sa.Column('Remarques_Vente', sa.Text(), nullable=True),
    sa.Column('Statut_Vente', sa.Text(), nullable=True),
    sa.Column('Fournisseur_Id', sa.String(length=255), nullable=True),
    sa.Column('Prescription_Requise', sa.Text(), nullable=True),
    sa.Column('Statut_Livraison', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('Vente_Id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ventes')
    op.drop_table('utilisateur')
    op.drop_table('serologie')
    op.drop_table('revenus')
    op.drop_table('rendezvous')
    op.drop_table('mouvements_medicaments')
    op.drop_table('mouvements_inventaire')
    op.drop_table('inventaire')
    op.drop_table('historique_rendezvous')
    op.drop_table('historique_patient')
    op.drop_table('historique_medicaments_pharmacie')
    op.drop_table('historique_factures')
    op.drop_table('historique_dossiers_medicaux')
    op.drop_table('fournisseurs')
    op.drop_table('fiches_prescription')
    op.drop_table('factures')
    op.drop_table('examens_selles')
    op.drop_table('examens_hemogramme')
    op.drop_table('examens_biochimie')
    op.drop_table('examen_urine')
    op.drop_table('dossier_medical')
    op.drop_table('depenses')
    op.drop_table('connexion')
    op.drop_table('alertes_reapprovisionnement_pharmacie')
    op.drop_table('alertes_reapprovisionnement')
    # ### end Alembic commands ###

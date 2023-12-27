# Importe les extensions nécessaires
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Initialise l'extension SQLAlchemy
db = SQLAlchemy()

# Modèle de la table des Patients
class Utilisateur(db.Model):
    User_Id = db.Column(db.String(255), primary_key=True)
    First_Name = db.Column(db.String(255))
    Last_Name = db.Column(db.String(255))
    Username = db.Column(db.String(255))
    Email = db.Column(db.String(255))
    Phone = db.Column(db.String(20))  # Utiliser String pour les numéros de téléphone
    Password = db.Column(db.String(255))
    Date_of_Creation = db.Column(db.Date)
    Account_Type = db.Column(db.String(50))

class Connexion(db.Model):
    Connexion_Id = db.Column(db.String(255), primary_key=True)
    User_Id = db.Column(db.String(255))
    Date_Time = db.Column(db.String(255))  # Vous pouvez utiliser le type approprié pour les dates/heure
    User = db.relationship('Utilisateur', backref='connexions')  # Relation avec la table Utilisateurs

class DossierMedical(db.Model):
    Patient_Id = db.Column(db.String(255), primary_key=True)
    Date_Ouverture_Dossier = db.Column(db.Date)
    Nom = db.Column(db.String(255))
    Prenom = db.Column(db.String(255))
    Date_Naissance = db.Column(db.Date)
    Genre = db.Column(db.String(50))
    Statut_Marital = db.Column(db.String(50))
    Email = db.Column(db.String(255))
    Telephone = db.Column(db.String(20))  # Utiliser String pour les numéros de téléphone
    Telephone2 = db.Column(db.String(20))  # Utiliser String pour les numéros de téléphone
    Adresse = db.Column(db.String(255))
    Religion = db.Column(db.String(50))
    Nationalite = db.Column(db.String(50))
    Groupe_Sanguin = db.Column(db.String(10))
    Hauteur = db.Column(db.Float)
    Poids = db.Column(db.Float)
    Methode_Paiement = db.Column(db.String(50))
    Tension_Arterielle = db.Column(db.Float)
    Rythme_Cardiaque = db.Column(db.Float)

class HistoriquePatient(db.Model):
    Historique_Patient_Id = db.Column(db.Integer, primary_key=True)
    Patient_Id = db.Column(db.String(255))
    Date_Heure_Modification = db.Column(db.Date)
    User_Id = db.Column(db.String(255))
    Champ_Modifie = db.Column(db.String(255))
    Valeur_Avant_Modification = db.Column(db.String(255))
    Nouvelle_Valeur = db.Column(db.String(255))
    User = db.relationship('Utilisateur', backref='historique_patients')  # Relation avec la table Utilisateurs
    Patient = db.relationship('DossierMedical', backref='historique_patients')  # Relation avec la table Dossier_Medical

class Inventaire(db.Model):
    Article_Id = db.Column(db.String(255), primary_key=True)
    Nom_Article = db.Column(db.String(255))
    Description_Article = db.Column(db.Text)
    Categorie_Id = db.Column(db.String(255))
    Quantite_Stock = db.Column(db.Integer)
    Quantite_Minimale_Souhaitee = db.Column(db.Integer)
    Prix_Unitaire = db.Column(db.Float)
    Date_Expiration = db.Column(db.String(255))

class MouvementsInventaire(db.Model):
    Mouvement_Id = db.Column(db.Integer, primary_key=True)
    Article_Id = db.Column(db.String(255))
    Type_Mouvement = db.Column(db.String(255))
    Date_Heure_Mouvement = db.Column(db.DateTime)
    Quantite_Impliquee = db.Column(db.Integer)
    User_Id = db.Column(db.String(255))
    Raison_Mouvement = db.Column(db.Text)
    Nouvelle_Quantite_Stock = db.Column(db.Integer)
    User = db.relationship('Utilisateur', backref='mouvements_inventaire')  # Relation avec la table Utilisateurs
    Article = db.relationship('Inventaire', backref='mouvements_inventaire')  # Relation avec la table Inventaire

class Fournisseurs(db.Model):
    Fournisseur_Id = db.Column(db.String(255), primary_key=True)
    Nom_Fournisseur = db.Column(db.String(255))
    Adresse = db.Column(db.Text)
    Numero_Telephone = db.Column(db.String(20))  # Utiliser String pour les numéros de téléphone
    Adresse_Email = db.Column(db.String(255))
    Produits_Fournis = db.Column(db.Text)

class AlertesReapprovisionnement(db.Model):
    Alerte_Id = db.Column(db.String(255), primary_key=True)
    Article_Id = db.Column(db.String(255))
    Quantite_Minimale_Souhaitee = db.Column(db.Integer)
    Quantite_Actuelle_Stock = db.Column(db.Integer)
    Date_Alerte = db.Column(db.Date)
    Statut_Alerte = db.Column(db.String(50))
    Numero_Lot_Medicament = db.Column(db.String(255))
    Fournisseur_Id = db.Column(db.String(255))
    Medicament_Commander = db.Column(db.String(255))
    Quantite_Commander = db.Column(db.Integer)
    Date_Commande = db.Column(db.Date)
    User_Id = db.Column(db.String(255))
    Remarques_Alerte = db.Column(db.Text)
    Statut_Traitement_Commande = db.Column(db.String(50))
    Date_Reception_Medicaments = db.Column(db.Date)
    User = db.relationship('Utilisateur', backref='alertes_reapprovisionnement')  # Relation avec la table Utilisateurs
    Fournisseur = db.relationship('Fournisseurs', backref='alertes_reapprovisionnement')  # Relation avec la table Fournisseurs

class Rendezvous(db.Model):
    Rendezvous_Id = db.Column(db.String(255), primary_key=True)
    Nom = db.Column(db.String(255))
    Prenom = db.Column(db.String(255))
    Patient_Id = db.Column(db.String(255))
    Date_Heure_Rendezvous = db.Column(db.DateTime)
    Duree_Rendezvous = db.Column(db.Integer)
    Motif_Rendezvous = db.Column(db.Text)
    User_Id = db.Column(db.String(255))
    Patient = db.relationship('DossierMedical', backref='rendezvous')  # Relation avec la table Dossier_Medical
    User = db.relationship('Utilisateur', backref='rendezvous')  # Relation avec la table Utilisateurs

class Factures(db.Model):
    Facture_Id = db.Column(db.String(255), primary_key=True)
    User_Id = db.Column(db.String(255))
    Patient_Id = db.Column(db.String(255))
    Nom = db.Column(db.String(255))
    Prenom = db.Column(db.String(255))
    Adresse = db.Column(db.String(255))
    Date_Facture = db.Column(db.Date)
    Montant_Total = db.Column(db.Float)
    Statut_Facture = db.Column(db.String(50))
    Date_Paiement = db.Column(db.Date)
    Methode_Paiement = db.Column(db.String(50))
    Description_Services_Produits = db.Column(db.Text)
    Numero_Facture = db.Column(db.String(255))
    Coordonnees_Clinique = db.Column(db.Text)
    Taxes = db.Column(db.Float)
    Remises = db.Column(db.Float)
    Details_Assurance = db.Column(db.Text)
    Numero_Reference_Paiement = db.Column(db.String(255))
    Notes_Commentaires = db.Column(db.Text)
    Type_Service_Produit = db.Column(db.String(50))
    Modes_Paiement_Acceptes = db.Column(db.Text)
    Documents_Attaches = db.Column(db.LargeBinary)
    Statut_Remboursement = db.Column(db.String(50))
    Responsable_Facturation = db.Column(db.String(255))
    Patient = db.relationship('DossierMedical', backref='factures')  # Relation avec la table Dossier_Medical
    User = db.relationship('Utilisateur', backref='factures')  # Relation avec la table Utilisateurs

class Revenus(db.Model):
    Revenu_Id = db.Column(db.Integer, primary_key=True)
    Source_Revenu = db.Column(db.String(255))
    Date_Revenu = db.Column(db.Date)
    Montant_Revenu = db.Column(db.Float)
    Type_Paiement = db.Column(db.String(50))
    Reference_Facture = db.Column(db.String(255))
    Responsable_Paiement = db.Column(db.String(255))
    Details_Transaction = db.Column(db.Text)
    Statut_Transaction = db.Column(db.String(50))
    Reference_Patient = db.Column(db.String(255))
    Mode_Facturation = db.Column(db.String(50))
    Categorie_Revenu = db.Column(db.String(50))
    Date_Saisie = db.Column(db.DateTime)
    Reference_Compte_Bancaire = db.Column(db.String(255))
    Methode_Facturation = db.Column(db.String(50))
    Heure_Transaction = db.Column(db.Time)
    Devise = db.Column(db.String(50))
    Taxes = db.Column(db.Float)
    Remises = db.Column(db.Float)
    Rapprochement_Bancaire = db.Column(db.String(255))

class Depenses(db.Model):
    Depense_Id = db.Column(db.String(255), primary_key=True)
    Categorie_Depense = db.Column(db.String(50))
    Date_Depense = db.Column(db.Date)
    Montant_Depense = db.Column(db.Float)
    Description_Depense = db.Column(db.Text)
    Numero_Facture_Reçu = db.Column(db.String(255))
    Methode_Paiement = db.Column(db.String(50))
    Responsable_Depense = db.Column(db.String(255))
    Devise = db.Column(db.String(50))
    Taxes = db.Column(db.Float)
    Remises = db.Column(db.Float)
    Lieu_Depense = db.Column(db.String(255))
    Fournisseur_ID = db.Column(db.String(255))
    Numero_Bon_Commande = db.Column(db.String(255))
    Statut_Depense = db.Column(db.String(50))
    Notes_Commentaires = db.Column(db.Text)
    Rapprochement_Comptable = db.Column(db.String(255))
    Type_Depense = db.Column(db.String(50))
    Date_Saisie = db.Column(db.DateTime)
    Nom_Fournisseur = db.Column(db.String(255))
    Fournisseur = db.relationship('Fournisseurs', backref='depenses')  # Relation avec la table Fournisseurs

class ExamensHemogramme(db.Model):
    Examen_Id = db.Column(db.String(255), primary_key=True)
    Nom = db.Column(db.String(255))
    Prenom = db.Column(db.String(255))
    Adresse = db.Column(db.String(255))
    Patient_Id = db.Column(db.String(255))
    Date_Test = db.Column(db.Date)
    User_Id = db.Column(db.String(255))
    Telephone = db.Column(db.String(20))  # Utiliser String pour les numéros de téléphone
    Globules_Rouges = db.Column(db.Text)
    Globules_Blancs = db.Column(db.Text)
    Hematocrite = db.Column(db.Text)
    Hemoglobine = db.Column(db.Text)
    MCV = db.Column(db.Text)
    MCH = db.Column(db.Text)
    MCHC = db.Column(db.Text)
    Polynucleaires = db.Column(db.Text)
    Lymphocytes = db.Column(db.Text)
    Monocytes = db.Column(db.Text)
    Eosinophiles = db.Column(db.Text)
    Basophiles = db.Column(db.Text)
    Reticulocytes = db.Column(db.Text)
    Plaquettes = db.Column(db.Text)
    Groupe_Sanguin = db.Column(db.Text)
    Test_Malaria = db.Column(db.Text)
    Test_Falciformation = db.Column(db.Text)
    Electrophorese_Hemoglobine = db.Column(db.Text)
    Phenotype_Groupe_Sanguin = db.Column(db.Text)
    Vitesse_Sedimentation = db.Column(db.Text)
    Temps_Saignement = db.Column(db.Text)
    Temps_Coagulation = db.Column(db.Text)
    PT = db.Column(db.Text)
    PTT = db.Column(db.Text)
    IRN = db.Column(db.Text)
    D_Dimeres = db.Column(db.Text)
    Fibrinogene = db.Column(db.Text)
    Troponine = db.Column(db.Text)
    CRP = db.Column(db.Text)
    Procalcitonine = db.Column(db.Text)
    Bilirubine_Totale = db.Column(db.Text)
    Bilirubine_Directe = db.Column(db.Text)
    Bilirubine_Indirecte = db.Column(db.Text)
    Lipides_Sanguins = db.Column(db.Text)
    Electrolytes = db.Column(db.Text)
    Marqueurs_Hormonaux = db.Column(db.Text)
    Tests_Allergies = db.Column(db.Text)
    Tests_Fonction_Renale = db.Column(db.Text)
    Tests_Coagulation = db.Column(db.Text)

    Patient = db.relationship('DossierMedical', backref='examens_hemogramme')  # Relation avec la table Dossier_Medical
    User = db.relationship('Utilisateur', backref='examens_hemogramme')  # Relation avec la table Utilisateurs

class ExamenUrine(db.Model):
    Examen_Id = db.Column(db.String(255), primary_key=True)
    User_Id = db.Column(db.String(255))
    Nom = db.Column(db.String(255))
    Prenom = db.Column(db.String(255))
    Adresse = db.Column(db.String(255))
    Patient_Id = db.Column(db.String(255))
    Couleur = db.Column(db.String(255))
    Telephone = db.Column(db.String(20))  # Utiliser String pour les numéros de téléphone
    Aspect = db.Column(db.String(255))
    Densite = db.Column(db.Float)
    pH = db.Column(db.Float)
    Glucose = db.Column(db.String(255))
    Proteinurie = db.Column(db.String(255))
    Cetone = db.Column(db.String(255))
    Bilirubinurie = db.Column(db.String(255))
    Nitrites = db.Column(db.String(255))
    Urobilinogene = db.Column(db.String(255))
    Microscopie = db.Column(db.String(255))
    Leucocytes = db.Column(db.String(255))
    Hematies = db.Column(db.String(255))
    CellulesEpitheliales = db.Column(db.String(255))
    Bacteries = db.Column(db.String(255))
    LevuresSimples = db.Column(db.String(255))
    LevuresBourgeonnantes = db.Column(db.String(255))
    CristauxOxalateCalcium = db.Column(db.String(255))
    CylindresLeucocytaires = db.Column(db.String(255))
    CylindresGranuleux = db.Column(db.String(255))
    TrichomonasVaginalis = db.Column(db.String(255))

    Patient = db.relationship('DossierMedical', backref='examens_urine')  # Relation avec la table Dossier_Medical
    User = db.relationship('Utilisateur', backref='examens_urine')  # Relation avec la table Utilisateurs

class ExamensBiochimie(db.Model):
    Examen_Id = db.Column(db.String(255), primary_key=True)
    Nom = db.Column(db.String(255))
    Prenom = db.Column(db.String(255))
    Adresse = db.Column(db.String(255))
    Patient_Id = db.Column(db.String(255))
    Date_Test = db.Column(db.Date)
    User_Id = db.Column(db.String(255))
    Telephone = db.Column(db.String(20))  # Utiliser String pour les numéros de téléphone
    Glycemie = db.Column(db.Text)
    Azote_Uree = db.Column(db.Text)
    Uree = db.Column(db.Text)
    Creatinine = db.Column(db.Text)
    BUN_Creatinine = db.Column(db.Text)
    Proteines_Totales = db.Column(db.Text)
    Albumine = db.Column(db.Text)
    Globuline = db.Column(db.Text)
    Rapport_Albumine_Globuline = db.Column(db.Text)
    Acide_Urique = db.Column(db.Text)
    Sodium = db.Column(db.Text)
    Potassium = db.Column(db.Text)
    Calcium = db.Column(db.Text)
    CO2 = db.Column(db.Text)
    Magnesium = db.Column(db.Text)
    Chlorure = db.Column(db.Text)
    Bilirubine_Totale = db.Column(db.Text)
    Bilirubine_Directe = db.Column(db.Text)
    Bilirubine_Indirecte = db.Column(db.Text)
    SGOT = db.Column(db.Text)
    SGPT = db.Column(db.Text)
    Phosphore = db.Column(db.Text)
    Cholesterol = db.Column(db.Text)
    HDL_Cholesterol = db.Column(db.Text)
    Triglycerides = db.Column(db.Text)
    VLDL_Cholesterol = db.Column(db.Text)
    LDL_Cholesterol = db.Column(db.Text)
    Phosphatase_Alcaline = db.Column(db.Text)
    Prolactine = db.Column(db.Text)
    Insuline = db.Column(db.Text)
    Hemoglobine_Glyquee = db.Column(db.Text)
    Fer_Serique = db.Column(db.Text)
    Ferritine = db.Column(db.Text)
    TLBC = db.Column(db.Text)
    FSH_LH = db.Column(db.Text)

    Patient = db.relationship('DossierMedical', backref='examens_biochimie')  # Relation avec la table Dossier_Medical
    User = db.relationship('Utilisateur', backref='examens_biochimie')  # Relation avec la table Utilisateurs

class ExamensSelles(db.Model):
    Examen_Id = db.Column(db.String(255), primary_key=True)
    Nom = db.Column(db.String(255))
    Prenom = db.Column(db.String(255))
    Adresse = db.Column(db.String(255))
    Patient_Id = db.Column(db.String(255))
    Date_Test = db.Column(db.Date)
    User_Id = db.Column(db.String(255))
    Telephone = db.Column(db.String(20))  # Utiliser String pour les numéros de téléphone
    Apparence_Selles = db.Column(db.Text)
    Consistance_Selles = db.Column(db.Text)
    Sang_Occulte = db.Column(db.Text)
    Oeufs_Parasites = db.Column(db.Text)
    Bleu_Methylene = db.Column(db.Text)

    Patient = db.relationship('DossierMedical', backref='examens_selles')  # Relation avec la table Dossier_Medical
    User = db.relationship('Utilisateur', backref='examens_selles')  # Relation avec la table Utilisateurs

class Serologie(db.Model):
    Examen_Id = db.Column(db.String(255), primary_key=True)
    Patient_Id = db.Column(db.String(255))
    Date_Examen = db.Column(db.Date)
    User_Id = db.Column(db.String(255))
    Nom = db.Column(db.String(255))
    Prenom = db.Column(db.String(255))
    Adresse = db.Column(db.String(255))
    Telephone = db.Column(db.String(20))  # Utiliser String pour les numéros de téléphone
    BHCG = db.Column(db.Text)
    RPR = db.Column(db.Text)
    HIV = db.Column(db.Text)
    CRP = db.Column(db.Text)
    ASO = db.Column(db.Text)
    PSA = db.Column(db.Text)
    Salmonella_O = db.Column(db.Text)
    Salmonella_H = db.Column(db.Text)
    H_Pyloric = db.Column(db.Text)
    Toxoplasma_IGG = db.Column(db.Text)
    Toxoplasma_IGM = db.Column(db.Text)
    Rubella_IGM = db.Column(db.Text)
    TPHA = db.Column(db.Text)
    Chlamydia_ICG = db.Column(db.Text)
    Chlamydia_IGM = db.Column(db.Text)
    Facteur_Rhumatoide = db.Column(db.Text)
    Mantoux_Test = db.Column(db.Text)
    Herpes_Type_I_IGG = db.Column(db.Text)
    Herpes_Type_II_IGG = db.Column(db.Text)
    Herpes_Type_II_IGM = db.Column(db.Text)
    Hbs_Ag = db.Column(db.Text)
    Hepatite_C = db.Column(db.Text)
    Mono_Test = db.Column(db.Text)
    Virus_Hepatite_B = db.Column(db.Text)
    Virus_Hepatite_C = db.Column(db.Text)
    Anticorps_VIH = db.Column(db.Text)
    Virus_Dengue = db.Column(db.Text)
    Virus_Zika = db.Column(db.Text)
    Virus_Fievre_Jaune = db.Column(db.Text)
    Virus_Rubeole = db.Column(db.Text)
    Anticorps_Toxoplasme = db.Column(db.Text)
    Virus_Grippe = db.Column(db.Text)
    Virus_Rougeole = db.Column(db.Text)
    Virus_Oreillons = db.Column(db.Text)

    Patient = db.relationship('DossierMedical', backref='serologie')  # Relation avec la table Dossier_Medical
    User = db.relationship('Utilisateur', backref='serologie')  # Relation avec la table Utilisateurs

class FichesPrescription(db.Model):
    Fiche_Prescription_Id = db.Column(db.String(255), primary_key=True)
    Patient_Id = db.Column(db.String(255))
    User_Id = db.Column(db.String(255))
    Date_Prescription = db.Column(db.Text)
    Medicament_Prescrit = db.Column(db.Text)
    Quantite_Prescrite = db.Column(db.Integer)
    Frequence_Prise = db.Column(db.Text)
    Instructions_Speciales = db.Column(db.Text)
    Statut_Prescription = db.Column(db.Text)
    Numero_Lot = db.Column(db.Text)
    Date_Debut_Traitement = db.Column(db.Text)
    Date_Fin_Traitement = db.Column(db.Text)
    Renouvellement_Prescription = db.Column(db.Text)
    Notes_Medecin = db.Column(db.Text)
    Statut_Validation = db.Column(db.Text)
    Rappels_Prescription = db.Column(db.Text)

    Patient = db.relationship('DossierMedical', backref='fiches_prescription')  # Relation avec la table Dossier_Medical
    User = db.relationship('Utilisateur', backref='fiches_prescription')  # Relation avec la table Utilisateurs

class Ventes(db.Model):
    Vente_Id = db.Column(db.String(255), primary_key=True)
    Article_Id = db.Column(db.String(255))
    Patient_Id = db.Column(db.String(255))
    User_Id = db.Column(db.String(255))
    Date_Vente = db.Column(db.Text)
    Quantite_Vendue = db.Column(db.Integer)
    Prix_Unitaire_Vente = db.Column(db.Float)
    Montant_Total_Vente = db.Column(db.Float)
    Numero_Lot_Medicament = db.Column(db.Text)
    Heure_Vente = db.Column(db.Text)
    Mode_Paiement = db.Column(db.Text)
    Remarques_Vente = db.Column(db.Text)
    Statut_Vente = db.Column(db.Text)
    Fournisseur_Id = db.Column(db.String(255))
    Prescription_Requise = db.Column(db.Text)
    Statut_Livraison = db.Column(db.Text)

    Article = db.relationship('Inventaire', backref='ventes')  # Relation avec la table Inventaire
    User = db.relationship('Utilisateur', backref='ventes')  # Relation avec la table Utilisateurs
    Fournisseur = db.relationship('Fournisseurs', backref='ventes')  # Relation avec la table Fournisseurs
    Patient = db.relationship('DossierMedical', backref='ventes')  # Relation avec la table Dossier_Medical

class MouvementsMedicaments(db.Model):
    Mouvement_Id = db.Column(db.String(255), primary_key=True)
    Article_Id = db.Column(db.String(255))
    Type_Mouvement = db.Column(db.Text)
    Date_Heure_Mouvement = db.Column(db.DateTime)
    Quantite_Impliquee = db.Column(db.Integer)
    User_Id = db.Column(db.String(255))
    Raison_Mouvement = db.Column(db.Text)
    Nouvelle_Quantite_Stock = db.Column(db.Integer)
    Numero_Lot_Medicament = db.Column(db.Text)
    Reference_Commande = db.Column(db.Text)
    Cout_Unitaire = db.Column(db.Float)
    Cout_Total = db.Column(db.Float)
    Stock_Minimum = db.Column(db.Integer)
    Statut_Validation = db.Column(db.Text)
    Fournisseur_Id = db.Column(db.String(255))
    Commande_Client_Id = db.Column(db.Text)
    Reference_Patient = db.Column(db.Text)
    Emplacement_Stockage = db.Column(db.Text)
    Methode_Stockage = db.Column(db.Text)
    Date_Expiration_Medicament = db.Column(db.Text)

    Article = db.relationship('Inventaire', backref='mouvements_medicaments')  # Relation avec la table Inventaire
    Fournisseur = db.relationship('Fournisseurs', backref='mouvements_medicaments')  # Relation avec la table Fournisseurs
    User = db.relationship('Utilisateur', backref='mouvements_medicaments')  # Relation avec la table Utilisateurs

class AlertesReapprovisionnementPharmacie(db.Model):
    Alerte_Id = db.Column(db.String(255), primary_key=True)
    Article_Id = db.Column(db.String(255))
    Quantite_Minimale_Souhaitee = db.Column(db.Integer)
    Quantite_Actuelle_Stock = db.Column(db.Integer)
    Date_Alerte = db.Column(db.Date)
    Statut_Alerte = db.Column(db.Text)
    Pharmacie_Id = db.Column(db.String(255))
    Numero_Lot_Medicament = db.Column(db.Text)
    Reference_Fournisseur = db.Column(db.Text)
    Medicament_Commander = db.Column(db.Text)
    Quantite_Commander = db.Column(db.Integer)
    Date_Commande = db.Column(db.Date)
    User_Id = db.Column(db.String(255))
    Remarques_Alerte = db.Column(db.Text)
    Statut_Traitement_Commande = db.Column(db.Text)
    Date_Reception_Medicaments = db.Column(db.Date)

    Article = db.relationship('Inventaire', backref='alertes_reapprovisionnement_pharmacie')  # Relation avec la table Inventaire
    User = db.relationship('Utilisateur', backref='alertes_reapprovisionnement_pharmacie')  # Relation avec la table Utilisateurs

db = SQLAlchemy()

class HistoriqueRendezvous(db.Model):
    Historique_Rendezvous_Id = db.Column(db.String(255), primary_key=True)
    Rendezvous_Id = db.Column(db.String(255))
    Date_Heure_Modification = db.Column(db.DateTime)
    User_Id = db.Column(db.String(255))
    Nouvelle_Date_Heure_Rendezvous = db.Column(db.DateTime)
    Motif_Modification = db.Column(db.Text)

    User = db.relationship('Utilisateur', backref='historique_rendezvous')  # Relation avec la table Utilisateurs
    Rendezvous = db.relationship('Rendezvous', backref='historique_rendezvous')  # Relation avec la table Rendezvous

class HistoriqueDossiersMedicaux(db.Model):
    Historique_Dossiers_Medicaux_Id = db.Column(db.String(255), primary_key=True)
    Patient_Id = db.Column(db.String(255))
    Date_Heure_Modification = db.Column(db.DateTime)
    User_Id = db.Column(db.String(255))
    Champ_Modifie = db.Column(db.Text)
    Valeur_Avant_Modification = db.Column(db.Text)
    Nouvelle_Valeur = db.Column(db.Text)

    User = db.relationship('Utilisateur', backref='historique_dossiers_medicaux')  # Relation avec la table Utilisateurs
    Patient = db.relationship('DossierMedical', backref='historique_dossiers_medicaux')  # Relation avec la table Dossier_Medical

class HistoriqueFactures(db.Model):
    Historique_Factures_Id = db.Column(db.String(255), primary_key=True)
    Facture_Id = db.Column(db.String(255))
    Date_Heure_Modification = db.Column(db.DateTime)
    User_Id = db.Column(db.String(255))
    Montant_Modifie = db.Column(db.Float)
    Motif_Modification = db.Column(db.Text)

    User = db.relationship('Utilisateur', backref='historique_factures')  # Relation avec la table Utilisateurs
    Facture = db.relationship('Factures', backref='historique_factures')  # Relation avec la table Factures

class HistoriqueMedicamentsPharmacie(db.Model):
    Historique_Medicaments_Pharmacie_Id = db.Column(db.String(255), primary_key=True)
    Article_Id = db.Column(db.String(255))
    Date_Heure_Modification = db.Column(db.DateTime)
    User_Id = db.Column(db.String(255))
    Champ_Modifie = db.Column(db.Text)
    Valeur_Avant_Modification = db.Column(db.Text)
    Nouvelle_Valeur = db.Column(db.Text)

    User = db.relationship('Utilisateur', backref='historique_medicaments_pharmacie')  # Relation avec la table Utilisateurs
    Article = db.relationship('Inventaire', backref='historique_medicaments_pharmacie')  # Relation avec la table Inventaire



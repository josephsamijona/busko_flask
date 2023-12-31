from flask import Blueprint, render_template, jsonify
from models import (
    DossierMedical, HistoriquePatient, Rendezvous,
    Inventaire, MouvementsInventaire, Fournisseurs, AlertesReapprovisionnement,
    Factures, Revenus, Depenses, Ventes
)
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import datetime, timedelta
import csv
import pandas as pd
from reportlab.pdfgen import canvas
import tempfile
from io import StringIO
from mpl_toolkits.basemap import Basemap


analytics = Blueprint('analytics', __name__)


 
class PatientAnalytics:
    def __init__(self):
        pass


    def get_patient_data(self):
        patients_data = DossierMedical.query.all()
        history_data = HistoriquePatient.query.all()
        appointments_data = Rendezvous.query.all()
        return patients_data, history_data, appointments_data
    
    def generate_demographics_chart(self, patients_data):
        # Calculer le total du nombre de patients
        total_patients = len(patients_data)

        # Créer un diagramme circulaire
        labels = ['Total des Patients', 'Autres']
        sizes = [total_patients, 0]  # 0 pour "Autres" car nous n'avons pas d'autres catégories ici

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'lightgray'])
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.title('Démographie des Patients')
        plt.show()
        pass
        

    def generate_age_distribution_chart(self, patients_data):
        # Obtenez les âges des patients
        ages = [patient.age for patient in patients_data if patient.age is not None]

        # Créez des intervalles d'âge
        bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

        # Générez l'histogramme
        plt.hist(ages, bins=bins, color='skyblue', edgecolor='black')
        plt.title('Répartition des Patients par Tranche d\'Âge')
        plt.xlabel('Âge')
        plt.ylabel('Nombre de Patients')
        plt.show()
        pass

    def generate_gender_distribution_chart(self, patients_data):
        # Obtenez les genres des patients
        genders = [patient.gender for patient in patients_data if patient.gender is not None]

        # Comptez le nombre de patients de chaque genre
        gender_counts = {gender: genders.count(gender) for gender in set(genders)}

        # Générez le diagramme circulaire
        labels = gender_counts.keys()
        sizes = gender_counts.values()

        plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['skyblue', 'lightcoral'])
        plt.title('Répartition des Patients par Genre')
        plt.show()
        pass

    def generate_geographic_distribution_chart(self, patients_data):
        # Exemple de carte géographique pour la répartition des patients par origine géographique
        # Utilisez les données appropriées pour générer la carte

        # Obtenez les coordonnées géographiques des patients (latitude, longitude)
        coordinates = [(patient.latitude, patient.longitude) for patient in patients_data
                       if patient.latitude is not None and patient.longitude is not None]

        # Générez la carte géographique
        plt.figure(figsize=(10, 8))
        m = Basemap(projection='mill', llcrnrlat=-60, urcrnrlat=85, llcrnrlon=-180, urcrnrlon=180, resolution='c')
        m.drawmapboundary(fill_color='#A6CAE0', linewidth=0)
        m.drawcoastlines(linewidth=0.5)
        m.drawcountries(linewidth=0.5)

        # Tracez les points sur la carte
        lats, lons = zip(*coordinates)
        x, y = m(lons, lats)
        m.scatter(x, y, s=50, color='red', alpha=0.7)

        plt.title('Répartition Géographique des Patients')
        plt.show()
        pass

     

    def generate_religion_nationality_chart(self, patients_data):
        # Exemple de diagramme en barres ou diagramme circulaire pour la répartition des patients par religion ou nationalité
        # Utilisez les données appropriées pour générer le graphique

        # Obtenez les données de religion ou nationalité des patients
        religion_nationality_data = [(patient.religion, patient.nationality) for patient in patients_data
                                      if patient.religion is not None and patient.nationality is not None]

        # Comptez le nombre de patients par religion ou nationalité
        religion_nationality_counts = {(religion, nationality): religion_nationality_data.count((religion, nationality))
                                       for religion, nationality in set(religion_nationality_data)}

        # Générez le diagramme en barres
        labels = [f"{religion}\n{nationality}" for religion, nationality in religion_nationality_counts.keys()]
        values = religion_nationality_counts.values()

        plt.bar(labels, values, color='skyblue')
        plt.title('Répartition des Patients par Religion ou Nationalité')
        plt.xlabel('Religion et Nationalité')
        plt.ylabel('Nombre de Patients')
        plt.xticks(rotation=45, ha='right')
        plt.show()

        # Ou générer le diagramme circulaire (décommentez le bloc ci-dessous)
        """
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        plt.title('Répartition des Patients par Religion ou Nationalité')
        plt.show()
        """
        pass

     
    def generate_blood_type_distribution_chart(self, patients_data):
       # Exemple de diagramme en barres pour la répartition des patients par groupe sanguin
        # Utilisez les données appropriées pour générer le graphique

        # Obtenez les données sur les groupes sanguins des patients
        blood_type_data = [patient.blood_type for patient in patients_data if patient.blood_type is not None]

        # Comptez le nombre de patients par groupe sanguin
        blood_type_counts = {blood_type: blood_type_data.count(blood_type) for blood_type in set(blood_type_data)}

        # Générez le diagramme en barres
        labels = list(blood_type_counts.keys())
        values = list(blood_type_counts.values())

        plt.bar(labels, values, color='skyblue')
        plt.title('Répartition des Patients par Groupe Sanguin')
        plt.xlabel('Groupe Sanguin')
        plt.ylabel('Nombre de Patients')
        plt.show()

        pass

    def generate_medical_parameters_correlation_chart(self, patients_data):
        # Exemple de matrice de corrélation ou nuage de points pour la corrélation entre paramètres médicaux
        # Utilisez les données appropriées pour générer le graphique

        # Obtenez les données sur les paramètres médicaux des patients
        medical_data = [
            {'weight': patient.weight, 'height': patient.height, 'blood_pressure': patient.blood_pressure}
            for patient in patients_data
        ]

        # Créez un DataFrame Pandas à partir des données
        df = pd.DataFrame(medical_data)

        # Générez la matrice de corrélation
        correlation_matrix = df.corr()

        # Affichez la matrice de corrélation sous forme de heatmap
        plt.figure(figsize=(8, 6))
        plt.imshow(correlation_matrix, cmap='coolwarm', interpolation='none', aspect='auto')
        plt.colorbar()
        plt.xticks(range(len(correlation_matrix)), correlation_matrix.columns, rotation='vertical')
        plt.yticks(range(len(correlation_matrix)), correlation_matrix.columns)
        plt.title('Matrice de Corrélation entre Paramètres Médicaux')
        plt.show()

        # Générez un nuage de points pour une paire spécifique de paramètres (par exemple, poids vs taille)
        plt.scatter(df['weight'], df['height'])
        plt.title('Corrélation entre Poids et Taille')
        plt.xlabel('Poids (kg)')
        plt.ylabel('Taille (cm)')
        plt.show()

        pass

    def generate_all_analytics(self):
        # Récupérer les données de la base de données
        patients_data, history_data, appointments_data = self.get_patient_data()

        # Générer des graphiques pour la section Patient
        
        self.generate_demographics_chart(patients_data)
        self.generate_age_distribution_chart(patients_data)
        self.generate_gender_distribution_chart(patients_data)
        self.generate_geographic_distribution_chart(patients_data)
        self.generate_religion_nationality_chart(patients_data)
        self.generate_blood_type_distribution_chart(patients_data)
        self.generate_medical_parameters_correlation_chart(patients_data)


class InventoryAnalytics:
    def __init__(self):
        pass

    def generate_inventory_levels_chart(self, inventory_data):
        # Exemple de graphique pour les niveaux d'inventaire
        inventory_levels = [item.quantity_in_stock for item in inventory_data]
        plt.bar(range(len(inventory_levels)), inventory_levels, color='green')
        plt.title('Niveaux d\'inventaire')
        plt.xlabel('Produits')
        plt.ylabel('Quantité en stock')
        plt.show()

    def generate_inventory_movements_chart(self, movements_data):
        # Ajoutez ici la logique pour générer un graphique des mouvements d'inventaire
        pass

    def generate_reorder_alerts_chart(self, alerts_data):
        # Ajoutez ici la logique pour générer un graphique des alertes de réapprovisionnement
        pass

    def generate_item_cost_chart(self, suppliers_data):
        # Ajoutez ici la logique pour générer un graphique du coût des articles
        pass

    def get_inventory_data(self):
        inventory_data = Inventaire.query.all()
        movements_data = MouvementsInventaire.query.all()
        suppliers_data = Fournisseurs.query.all()
        alerts_data = AlertesReapprovisionnement.query.all()
        return inventory_data, movements_data, suppliers_data, alerts_data

    def generate_all_analytics(self):
        # Récupérer les données de la base de données
        inventory_data, movements_data, suppliers_data, alerts_data = self.get_inventory_data()

        # Générer des graphiques pour la section Inventaire
        self.generate_inventory_levels_chart(inventory_data)
        self.generate_inventory_movements_chart(movements_data)
        self.generate_reorder_alerts_chart(alerts_data)
        self.generate_item_cost_chart(suppliers_data)

class FinanceAnalytics:
    def __init__(self):
        pass

    def generate_invoice_tracking_chart(self, invoices_data):
        # Exemple de graphique pour le suivi des factures
        invoice_amounts = [invoice.amount for invoice in invoices_data]
        plt.plot(range(len(invoice_amounts)), invoice_amounts, marker='o', color='purple')
        plt.title('Suivi des factures')
        plt.xlabel('Factures')
        plt.ylabel('Montant')
        plt.show()

    def generate_income_expense_chart(self, income_data, expenses_data):
        # Ajoutez ici la logique pour générer un graphique des revenus et des dépenses
        pass

    def generate_sales_margins_chart(self, sales_data):
        # Ajoutez ici la logique pour générer un graphique des ventes et des marges
        pass

    def generate_payment_analysis_chart(self):
        # Ajoutez ici la logique pour générer un graphique de l'analyse des modes de paiement
        pass

    def get_finance_data(self):
        invoices_data = Factures.query.all()
        income_data = Revenus.query.all()
        expenses_data = Depenses.query.all()
        sales_data = Ventes.query.all()
        return invoices_data, income_data, expenses_data, sales_data

    def generate_all_analytics(self):
        # Récupérer les données de la base de données
        invoices_data, income_data, expenses_data, sales_data = self.get_finance_data()

        # Générer des graphiques pour la section Finance
        self.generate_invoice_tracking_chart(invoices_data)
        self.generate_income_expense_chart(income_data, expenses_data)
        self.generate_sales_margins_chart(sales_data)
        self.generate_payment_analysis_chart()

class LabAnalytics:
    def __init__(self):
        pass

    def generate_test_results_chart(self, test_results):
        # Exemple de graphique pour les résultats des examens
        # Ajoutez ici la logique pour générer le graphique
        pass

    def generate_test_frequency_chart(self, test_frequency):
        # Exemple de graphique pour la fréquence des tests
        # Ajoutez ici la logique pour générer le graphique
        pass

    def generate_result_comparison_chart(self, result_comparison):
        # Exemple de graphique pour la comparaison des résultats
        # Ajoutez ici la logique pour générer le graphique
        pass

    def get_lab_data(self):
        #test_results = ResultatsExamens.query.all()
        #test_frequency = FrequencesTests.query.all()
        #result_comparison = ComparaisonResultats.query.all()
        return #test_results, test_frequency, result_comparison

    def generate_all_analytics(self):
        # Récupérer les données de la base de données
        test_results, test_frequency, result_comparison = self.get_lab_data()

        # Générer des graphiques pour la section Labo
        self.generate_test_results_chart(test_results)
        self.generate_test_frequency_chart(test_frequency)
        self.generate_result_comparison_chart(result_comparison)

class DataFilter:
    def __init__(self):
        pass

    @staticmethod
    def filter_by_date(data, start_date, end_date):
        # Filtrer les données par date
        filtered_data = [item for item in data if start_date <= item.date <= end_date]
        return filtered_data

    @staticmethod
    def filter_by_category(data, category):
        # Filtrer les données par catégorie
        filtered_data = [item for item in data if item.category == category]
        return filtered_data

    @staticmethod
    def filter_by_supplier(data, supplier):
        # Filtrer les données par fournisseur
        filtered_data = [item for item in data if item.supplier == supplier]
        return filtered_data

class DataComparator:
    def __init__(self, data):
        self.data = data

    def filter_by_date_range(self, start_date, end_date):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)  # Add one day to include the end date
        return [entry for entry in self.data if start_date <= entry['date'] < end_date]

    def compare_periods(self, data1, data2, period_name1, period_name2, chart_title):
        # Code pour comparer les périodes et afficher les données comparatives
        # Utilisez les bibliothèques de visualisation comme matplotlib ou seaborn
        pass

class DataExport:
    def __init__(self, data):
        self.data = data

    def export_to_csv(self, filename):
        # Fonction pour exporter les données au format CSV
        try:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = self.data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.data)
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False

    def export_to_excel(self, filename):
        # Fonction pour exporter les données au format Excel
        # Implémentez votre logique d'exportation vers Excel ici
        pass

    def export_to_pdf(self, filename, chart_image=None):
        # Fonction pour exporter les données au format PDF
        try:
            packet = StringIO()
            can = canvas.Canvas(packet)

            # Ajouter du texte ou des graphiques au PDF
            can.drawString(100, 100, "Rapport PDF")
            if chart_image:
                can.drawInlineImage(chart_image, 100, 200)

            can.save()

            # Move to the beginning of the StringIO buffer
            packet.seek(0)
            return packet
        except Exception as e:
            print(f"Error exporting to PDF: {e}")
            return None

    def save_pdf(self, packet, filename):
        # Fonction pour sauvegarder le PDF sur le disque
        try:
            with open(filename, 'wb') as pdf_file:
                pdf_file.write(packet.getvalue())
            return True
        except Exception as e:
            print(f"Error saving PDF: {e}")
            return False

class PredictiveAnalytics:
    def __init__(self, data):
        self.data = data

    def preprocess_data(self):
        # Fonction pour prétraiter les données en vue de l'analyse prédictive
        # Ici, nous convertissons les dates en jours depuis une date de référence
        reference_date = datetime(2023, 1, 1)
        self.data['days_since_reference'] = (self.data['date'] - reference_date).dt.days

    def train_predictive_model(self):
        # Séparation des données en ensemble d'entraînement et ensemble de test
        X = self.data[['days_since_reference']]
        y = self.data['target_variable']  # Remplacez par la variable cible réelle

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Création et entraînement du modèle
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Prédictions sur l'ensemble de test
        predictions = model.predict(X_test)

        return X_test, predictions

    def plot_predictions(self, X_test, predictions):
        # Fonction pour afficher les prédictions dans un graphique
        plt.scatter(X_test['days_since_reference'], predictions, label='Predictions', color='red')
        plt.xlabel('Days Since Reference Date')
        plt.ylabel('Target Variable')
        plt.title('Predictive Analytics')
        plt.legend()
        plt.show()

############### gestion des routes
 
data_filter = DataFilter()
period_comparison = DataComparator()
data_export = DataExport()
predictive_analysis = PredictiveAnalytics()
patient_analytics = PatientAnalytics()
inventory_analytics = InventoryAnalytics()
finance_analytics = FinanceAnalytics()
lab_analytics = LabAnalytics()

@analytics.route('/analytics', methods=['GET'])
def get_analytics():
    # Logique pour générer et récupérer des analyses
    return "Analyses"

@analytics.route('/filter', methods=['POST'])
def filter_data():
    # Exemple d'utilisation du filtre de données
    #filters = request.json  # Supposons que les filtres sont passés en tant que données JSON
    #filtered_data = data_filter.apply_filters(filters)
    return #jsonify(filtered_data)

@analytics.route('/compare_periods', methods=['POST'])
def compare_periods():
    # Exemple d'utilisation de la comparaison de périodes
    #comparison_data = #request.json  # Supposons que les données de comparaison sont passées en tant que données JSON
    #compared_data = period_comparison.compare_periods(comparison_data)
    return #jsonify(compared_data)

@analytics.route('/export_data', methods=['POST'])
def export_data():
    # Exemple d'utilisation de l'exportation de données
    #export_options = #request.json  # Supposons que les options d'exportation sont passées en tant que données JSON
    #exported_file = data_export.export_data(export_options)
    return #jsonify({'file_path': exported_file})

@analytics.route('/predictive_analytics', methods=['GET'])
def get_predictive_analytics():
    # Exemple d'utilisation de l'analyse prédictive
    #X_test, predictions = predictive_analytics.train_predictive_model()
    #predictive_analytics.plot_predictions(X_test, predictions)
    return jsonify({'message': 'Predictive analytics generated'})

@analytics.route('/patient', methods=['GET'])
def get_patient_analytics():
    # Exemple d'utilisation de la classe PatientAnalytics
    patient_data = patient_analytics.get_patient_data()
    frequency_data = patient_analytics.get_visit_frequency()
    disease_evolution = patient_analytics.get_disease_evolution()
    treatment_comparison = patient_analytics.compare_treatments()

    return jsonify({
        'patient_data': patient_data,
        'frequency_data': frequency_data,
        'disease_evolution': disease_evolution,
        'treatment_comparison': treatment_comparison
    })

@analytics.route('/inventory', methods=['GET'])
def get_inventory_analytics():
    # Exemple d'utilisation de la classe InventoryAnalytics
    inventory_levels = inventory_analytics.get_inventory_levels()
    movements_data = inventory_analytics.get_inventory_movements()
    alerts = inventory_analytics.get_reorder_alerts()
    cost_data = inventory_analytics.get_item_cost()

    return jsonify({
        'inventory_levels': inventory_levels,
        'movements_data': movements_data,
        'alerts': alerts,
        'cost_data': cost_data
    })

@analytics.route('/finance', methods=['GET'])
def get_finance_analytics():
    # Exemple d'utilisation de la classe FinanceAnalytics
    invoice_data = finance_analytics.get_invoice_tracking()
    income_expense_data = finance_analytics.get_income_expense_data()
    sales_margins = finance_analytics.get_sales_margins()
    payment_analysis = finance_analytics.get_payment_analysis()

    return jsonify({
        'invoice_data': invoice_data,
        'income_expense_data': income_expense_data,
        'sales_margins': sales_margins,
        'payment_analysis': payment_analysis
    })

@analytics.route('/lab', methods=['GET'])
def get_lab_analytics():
    # Exemple d'utilisation de la classe LabAnalytics
    test_results = lab_analytics.get_test_results()
    test_frequency = lab_analytics.get_test_frequency()
    result_comparison = lab_analytics.compare_results()

    return jsonify({
        'test_results': test_results,
        'test_frequency': test_frequency,
        'result_comparison': result_comparison
    })


if __name__ == "__main__":
    # Créer une instance de chaque classe d'Analytics
    patient_analytics = PatientAnalytics()
    inventory_analytics = InventoryAnalytics()
    finance_analytics = FinanceAnalytics()
    lab_analytics = LabAnalytics()

    # Générer les analytics pour chaque section
    patient_analytics.generate_all_analytics()
    inventory_analytics.generate_all_analytics()
    finance_analytics.generate_all_analytics()
    lab_analytics.generate_all_analytics()
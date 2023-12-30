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


analytic = Blueprint('analytic', __name__)



 

class AnalyticsGenerator:
    def __init__(self):
        pass

    def generate_patient_analytics(self, patients_data, history_data, appointments_data):
        # Exemple de graphique pour la fréquence des visites des patients
        patient_visits = [len(patient.appointments) for patient in patients_data]
        plt.hist(patient_visits, bins=20, color='skyblue', edgecolor='black')
        plt.title('Fréquence des visites des patients')
        plt.xlabel('Nombre de visites')
        plt.ylabel('Nombre de patients')
        plt.show()

        # Ajoutez d'autres exemples de graphiques pour la section des patients

    def generate_inventory_analytics(self, inventory_data, movements_data, suppliers_data, alerts_data):
        # Exemple de graphique pour les niveaux d'inventaire
        inventory_levels = [item.quantity_in_stock for item in inventory_data]
        plt.bar(range(len(inventory_levels)), inventory_levels, color='green')
        plt.title('Niveaux d\'inventaire')
        plt.xlabel('Produits')
        plt.ylabel('Quantité en stock')
        plt.show()

        # Ajoutez d'autres exemples de graphiques pour la section de l'inventaire

    def generate_finance_analytics(self, invoices_data, income_data, expenses_data, sales_data):
        # Exemple de graphique pour le suivi des factures
        invoice_amounts = [invoice.amount for invoice in invoices_data]
        plt.plot(range(len(invoice_amounts)), invoice_amounts, marker='o', color='purple')
        plt.title('Suivi des factures')
        plt.xlabel('Factures')
        plt.ylabel('Montant')
        plt.show()

        # Ajoutez d'autres exemples de graphiques pour la section financière

    def get_patient_data(self):
        patients_data = DossierMedical.query.all()
        history_data = HistoriquePatient.query.all()
        appointments_data = Rendezvous.query.all()
        return patients_data, history_data, appointments_data

    def get_inventory_data(self):
        inventory_data = Inventaire.query.all()
        movements_data = MouvementsInventaire.query.all()
        suppliers_data = Fournisseurs.query.all()
        alerts_data = AlertesReapprovisionnement.query.all()
        return inventory_data, movements_data, suppliers_data, alerts_data

    def get_finance_data(self):
        invoices_data = Factures.query.all()
        income_data = Revenus.query.all()
        expenses_data = Depenses.query.all()
        sales_data = Ventes.query.all()
        return invoices_data, income_data, expenses_data, sales_data

    def generate_all_analytics(self):
        # Récupérer les données de la base de données
        patients_data, history_data, appointments_data = self.get_patient_data()
        inventory_data, movements_data, suppliers_data, alerts_data = self.get_inventory_data()
        invoices_data, income_data, expenses_data, sales_data = self.get_finance_data()

        # Générer des graphiques pour chaque section
        self.generate_patient_analytics(patients_data, history_data, appointments_data)
        self.generate_inventory_analytics(inventory_data, movements_data, suppliers_data, alerts_data)
        self.generate_finance_analytics(invoices_data, income_data, expenses_data, sales_data)

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
analytics_generator = AnalyticsGenerator()
data_filter = DataFilter()
period_comparison = PeriodComparison()
data_export = DataExport()
predictive_analysis = PredictiveAnalysis()
patient_analytics = PatientAnalytics()
inventory_analytics = InventoryAnalytics()
finance_analytics = FinanceAnalytics()
lab_analytics = LabAnalytics()

@analytic.route('/analytics', methods=['GET'])
def get_analytics():
    # Logique pour générer et récupérer des analyses
    return "Analyses"

@analytics.route('/filter', methods=['POST'])
def filter_data():
    # Exemple d'utilisation du filtre de données
    filters = request.json  # Supposons que les filtres sont passés en tant que données JSON
    filtered_data = data_filter.apply_filters(filters)
    return jsonify(filtered_data)

@analytics.route('/compare_periods', methods=['POST'])
def compare_periods():
    # Exemple d'utilisation de la comparaison de périodes
    comparison_data = request.json  # Supposons que les données de comparaison sont passées en tant que données JSON
    compared_data = period_comparison.compare_periods(comparison_data)
    return jsonify(compared_data)

@analytics.route('/export_data', methods=['POST'])
def export_data():
    # Exemple d'utilisation de l'exportation de données
    export_options = request.json  # Supposons que les options d'exportation sont passées en tant que données JSON
    exported_file = data_export.export_data(export_options)
    return jsonify({'file_path': exported_file})

@analytics.route('/predictive_analytics', methods=['GET'])
def get_predictive_analytics():
    # Exemple d'utilisation de l'analyse prédictive
    X_test, predictions = predictive_analytics.train_predictive_model()
    predictive_analytics.plot_predictions(X_test, predictions)
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
    # Créer une instance de la classe AnalyticsGenerator
    analytics_generator = AnalyticsGenerator()

    # Appeler la méthode pour générer tous les analytics
    analytics_generator.generate_all_analytics()
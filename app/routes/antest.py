from flask import Blueprint, render_template
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
#from flask_socketio import SocketIO
import csv
import pandas as pd
from reportlab.pdfgen import canvas
import tempfile

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

if __name__ == "__main__":
    # Créer une instance de la classe AnalyticsGenerator
    analytics_generator = AnalyticsGenerator()

    # Appeler la méthode pour générer tous les analytics
    analytics_generator.generate_all_analytics()
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
from collections import Counter
from collections import defaultdict


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


    def generate_article_quantity_by_category_chart(self, inventory_data):
        
        categories = [item.category for item in inventory_data]
        quantity = [item.quantity for item in inventory_data]
        plt.bar(categories, quantity, color='skyblue')
        plt.title('Quantité d\'articles par catégorie')
        plt.xlabel('Catégorie')
        plt.ylabel('Quantité')
        plt.xticks(rotation=45, ha='right')  # Ajustez l'angle et l'alignement des étiquettes sur l'axe des x
        plt.show()        
                
        pass

    def generate_current_stock_per_item_chart(self, inventory_data):
        # Exemple de graphique pour le stock actuel par article (diagramme à barres empilées)
        items = [item.name for item in inventory_data]
        current_stock = [item.quantity_in_stock for item in inventory_data]
        minimum_stock = [item.minimum_quantity for item in inventory_data]

        fig, ax = plt.subplots()
        ax.bar(items, current_stock, label='Stock actuel', color='skyblue')
        ax.bar(items, minimum_stock, label='Quantité minimale', color='orange', alpha=0.7)

        plt.title('Stock actuel par article')
        plt.xlabel('Article')
        plt.ylabel('Quantité')
        plt.xticks(rotation=45, ha='right')  # Ajustez l'angle et l'alignement des étiquettes sur l'axe des x
        plt.legend()
        plt.show()
        
        pass

    def generate_top_n_most_active_articles_chart(self, movements_data, n=5):
       # Exemple de graphique pour le top N des articles les plus mouvementés
        articles = [movement.article_name for movement in movements_data]
        movement_counts = Counter(articles)
        top_n_articles = dict(movement_counts.most_common(n))

        plt.bar(top_n_articles.keys(), top_n_articles.values(), color='skyblue')
        plt.title(f'Top {n} des articles les plus mouvementés')
        plt.xlabel('Article')
        plt.ylabel('Nombre de mouvements')
        plt.xticks(rotation=45, ha='right')  # Ajustez l'angle et l'alignement des étiquettes sur l'axe des x
        plt.show()
        pass

    def generate_movement_distribution_by_type_chart(self, movements_data):
        # Exemple de graphique pour la répartition des mouvements d'inventaire par type
        movement_types = [movement.type for movement in movements_data]
        movement_type_counts = Counter(movement_types)

        plt.pie(movement_type_counts.values(), labels=movement_type_counts.keys(), autopct='%1.1f%%', colors=['skyblue', 'lightcoral'])
        plt.title('Répartition des mouvements d\'inventaire par type')
        plt.show()
        pass

    def generate_inventory_history_by_article_chart(self, movements_data):
        # Exemple de graphique pour l'historique des mouvements d'inventaire par article
        article_history = defaultdict(list)

        for movement in movements_data:
            article_history[movement.article_name].append((movement.date, movement.quantity))

        # Tracer l'historique pour chaque article
        for article, history in article_history.items():
            dates, quantities = zip(*history)
            plt.plot(dates, quantities, label=article, marker='o')

        plt.title('Historique des mouvements d\'inventaire par article')
        plt.xlabel('Date')
        plt.ylabel('Quantité')
        plt.legend()
        plt.show()
        pass

    def generate_top_n_most_active_medicines_chart(self, movements_data, n=5):
        # Exemple de graphique pour le top N des médicaments les plus mouvementés
        medicine_counter = Counter(movement.article_name for movement in movements_data)
        top_n_medicines = medicine_counter.most_common(n)

        medicine_names, counts = zip(*top_n_medicines)

        plt.bar(medicine_names, counts, color='blue')
        plt.title(f'Top {n} des médicaments les plus mouvementés')
        plt.xlabel('Médicament')
        plt.ylabel('Nombre de mouvements')
        plt.show()
        pass

    def generate_order_reception_evolution_chart(self, movements_data):
        # Exemple de graphique pour l'évolution des commandes et réceptions de médicaments
        ordered_dates = [movement.date for movement in movements_data if movement.type == 'Order']
        received_dates = [movement.date for movement in movements_data if movement.type == 'Reception']

        ordered_counts = Counter(map(lambda x: x.date(), ordered_dates))
        received_counts = Counter(map(lambda x: x.date(), received_dates))

        all_dates = sorted(set(ordered_counts.keys()) | set(received_counts.keys()))

        ordered_values = [ordered_counts[date] for date in all_dates]
        received_values = [received_counts[date] for date in all_dates]

        plt.plot(all_dates, ordered_values, label='Commandes', marker='o')
        plt.plot(all_dates, received_values, label='Réceptions', marker='o')

        plt.title('Évolution des commandes et réceptions de médicaments')
        plt.xlabel('Date')
        plt.ylabel('Nombre')
        plt.legend()
        plt.show()
        pass

    def generate_quantity_vs_minimum_by_article_chart(self, inventory_data):
        # Exemple de graphique pour la quantité actuelle vs quantité minimale souhaitée par article
        articles = [item.name for item in inventory_data]
        current_quantities = [item.quantity_in_stock for item in inventory_data]
        minimum_quantities = [item.minimum_quantity for item in inventory_data]

        x = range(len(articles))
        width = 0.35

        fig, ax = plt.subplots()
        rects1 = ax.bar(x, current_quantities, width, label='Quantité Actuelle')
        rects2 = ax.bar([i + width for i in x], minimum_quantities, width, label='Quantité Minimale Souhaitée')

        ax.set_xlabel('Articles')
        ax.set_ylabel('Quantité')
        ax.set_title('Quantité actuelle vs Quantité minimale souhaitée par article')
        ax.set_xticks([i + width / 2 for i in x])
        ax.set_xticklabels(articles)
        ax.legend()

        plt.show()
        pass

    def generate_supplier_distribution_by_product_chart(self, suppliers_data):
       # Exemple de graphique pour la distribution des fournisseurs par produits fournis
        products_supplied = [supplier.product_supplied for supplier in suppliers_data]

        # Count occurrences of each product
        product_counts = Counter(products_supplied)

        # Extract data for the chart
        products = list(product_counts.keys())
        counts = list(product_counts.values())

        # Plotting
        plt.bar(products, counts, color='blue')
        plt.xlabel('Produits')
        plt.ylabel('Nombre de fournisseurs')
        plt.title('Distribution des fournisseurs par produits fournis')
        plt.xticks(rotation=45, ha='right')
        plt.show()
        pass

    def generate_articles_without_replenishment_alerts_chart(self, inventory_data):
        # Exemple de graphique pour les articles sans alertes de réapprovisionnement
        # Utilisez les données appropriées pour générer le graphique

        # Filter inventory data to get items without replenishment alerts
        items_without_alerts = [item for item in inventory_data if item.replenishment_alert is None]

        # Extract data for the chart
        item_names = [item.name for item in items_without_alerts]
        quantities = [item.quantity_in_stock for item in items_without_alerts]

        # Plotting
        plt.bar(item_names, quantities, color='green')
        plt.xlabel('Articles')
        plt.ylabel('Quantité en stock')
        plt.title('Articles sans alertes de réapprovisionnement')
        plt.xticks(rotation=45, ha='right')
        plt.show()
        pass

    def generate_expired_medicines_stock_chart(self, inventory_data):
        # Exemple de graphique pour le stock actuel des médicaments expirés
        # Utilisez les données appropriées pour générer le graphique

        # Filter inventory data to get expired medicines
        expired_medicines = [item for item in inventory_data if item.expiry_date is not None and item.expiry_date < datetime.now()]

        # Extract data for the chart
        medicine_names = [item.name for item in expired_medicines]
        quantities = [item.quantity_in_stock for item in expired_medicines]

        # Plotting
        plt.bar(medicine_names, quantities, color='red')
        plt.xlabel('Médicaments')
        plt.ylabel('Quantité en stock')
        plt.title('Stock actuel des médicaments expirés')
        plt.xticks(rotation=45, ha='right')
        plt.show()
        pass

    def generate_medicine_movement_distribution_by_lot_chart(self, movements_data):
        # Exemple de graphique pour la répartition des mouvements de médicaments par numéro de lot
        # Utilisez les données appropriées pour générer le graphique

        # Extract data for the chart
        lot_numbers = [movement.lot_number for movement in movements_data]
        frequencies = Counter(lot_numbers)

        # Plotting
        plt.bar(frequencies.keys(), frequencies.values(), color='blue')
        plt.xlabel('Numéro de Lot')
        plt.ylabel('Fréquence de Mouvements')
        plt.title('Répartition des mouvements de médicaments par numéro de lot')
        plt.xticks(rotation=45, ha='right')
        plt.show()
        pass

    def generate_total_cost_of_medicine_movements_by_supplier_chart(self, movements_data):
        # Exemple de graphique pour le coût total des mouvements de médicaments par fournisseur
        # Utilisez les données appropriées pour générer le graphique

        # Extract data for the chart
        suppliers = [movement.supplier_name for movement in movements_data]
        costs = [movement.cost for movement in movements_data]

        # Calculate total cost per supplier
        total_costs = Counter()
        for supplier, cost in zip(suppliers, costs):
            total_costs[supplier] += cost

        # Plotting
        plt.bar(total_costs.keys(), total_costs.values(), color='green')
        plt.xlabel('Fournisseur')
        plt.ylabel('Coût Total des Mouvements')
        plt.title('Coût total des mouvements de médicaments par fournisseur')
        plt.xticks(rotation=45, ha='right')
        plt.show()
        pass

    def generate_medicine_movement_distribution_by_pharmacy_chart(self, movements_data):
       # Exemple de graphique pour la répartition des mouvements de médicaments par pharmacie
        # Utilisez les données appropriées pour générer le graphique

        # Extract data for the chart
        pharmacies = [movement.pharmacy_name for movement in movements_data]
        counts = Counter(pharmacies)

        # Plotting
        plt.bar(counts.keys(), counts.values(), color='blue')
        plt.xlabel('Pharmacie')
        plt.ylabel('Nombre de Mouvements de Médicaments')
        plt.title('Répartition des mouvements de médicaments par pharmacie')
        plt.xticks(rotation=45, ha='right')
        plt.show()
        pass

    def generate_specific_medicine_stock_evolution_by_pharmacy_chart(self, movements_data, medicine_id):
        # Exemple de graphique pour l'évolution du stock d'un médicament spécifique par pharmacie
        # Utilisez les données appropriées pour générer le graphique

        # Extract data for the chart
        data_by_pharmacy = defaultdict(list)
        for movement in movements_data:
            if movement.medicine_id == medicine_id:
                timestamp = datetime.strptime(movement.timestamp, '%Y-%m-%d %H:%M:%S')
                data_by_pharmacy[movement.pharmacy_name].append((timestamp, movement.stock_quantity))

        # Plotting
        for pharmacy, data in data_by_pharmacy.items():
            data.sort(key=lambda x: x[0])
            timestamps, stock_quantities = zip(*data)
            plt.plot(timestamps, stock_quantities, label=pharmacy)

        plt.xlabel('Date')
        plt.ylabel('Stock du Médicament spécifique')
        plt.title('Évolution du stock d\'un médicament spécifique par pharmacie')
        plt.legend()
        plt.show()
        pass

    def generate_replenishment_alert_distribution_by_pharmacy_chart(self, inventory_data):
        # Exemple de graphique pour la répartition des alertes de réapprovisionnement par pharmacie
        # Utilisez les données appropriées pour générer le graphique

        # Extracting data for the chart
        pharmacy_alerts = {}
        for item in inventory_data:
            pharmacy = item.pharmacy_name
            if item.replenishment_alert:
                if pharmacy in pharmacy_alerts:
                    pharmacy_alerts[pharmacy] += 1
                else:
                    pharmacy_alerts[pharmacy] = 1

        # Plotting
        if pharmacy_alerts:
            plt.bar(pharmacy_alerts.keys(), pharmacy_alerts.values())
            plt.xlabel('Pharmacie')
            plt.ylabel('Nombre d\'Alertes de Réapprovisionnement')
            plt.title('Répartition des alertes de réapprovisionnement par pharmacie')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()
        else:
            print('Aucune alerte de réapprovisionnement trouvée.')
        pass

    def generate_quantity_vs_minimum_by_medicine_pharmacy_chart(self, inventory_data):
        # Exemple de graphique pour la quantité actuelle vs quantité minimale souhaitée par médicament par pharmacie
        # Utilisez les données appropriées pour générer le graphique

        # Extracting data for the chart
        medicine_data = {}  # Assuming inventory_data is a list of objects with relevant attributes
        for item in inventory_data:
            medicine = item.medicine_name
            pharmacy = item.pharmacy_name
            current_quantity = item.current_quantity
            minimum_quantity = item.minimum_quantity

            if medicine not in medicine_data:
                medicine_data[medicine] = {'pharmacies': [], 'current_quantity': [], 'minimum_quantity': []}

            medicine_data[medicine]['pharmacies'].append(pharmacy)
            medicine_data[medicine]['current_quantity'].append(current_quantity)
            medicine_data[medicine]['minimum_quantity'].append(minimum_quantity)

        # Plotting
        for medicine, data in medicine_data.items():
            plt.figure(figsize=(10, 6))
            plt.bar(data['pharmacies'], data['current_quantity'], label='Quantité Actuelle')
            plt.bar(data['pharmacies'], data['minimum_quantity'], label='Quantité Minimale Souhaitée', alpha=0.7)

            plt.xlabel('Pharmacie')
            plt.ylabel('Quantité')
            plt.title(f'Quantité Actuelle vs Quantité Minimale Souhaitée pour {medicine}')
            plt.legend()
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()
        pass

    def generate_medicine_movement_distribution_by_user_pharmacy_chart(self, movements_data):
        # Exemple de graphique pour la répartition des mouvements de médicaments par utilisateur par pharmacie
        # Utilisez les données appropriées pour générer le graphique

        # Extracting data for the chart
        user_pharmacy_data = {}  # Assuming movements_data is a list of objects with relevant attributes
        for movement in movements_data:
            user = movement.user_name
            pharmacy = movement.pharmacy_name
            quantity = movement.quantity

            if user not in user_pharmacy_data:
                user_pharmacy_data[user] = {'pharmacies': [], 'quantity': []}

            user_pharmacy_data[user]['pharmacies'].append(pharmacy)
            user_pharmacy_data[user]['quantity'].append(quantity)

        # Plotting
        for user, data in user_pharmacy_data.items():
            plt.figure(figsize=(10, 6))
            plt.bar(data['pharmacies'], data['quantity'], label='Quantité de Mouvement')

            plt.xlabel('Pharmacie')
            plt.ylabel('Quantité')
            plt.title(f'Répartition des Mouvements de Médicaments par Utilisateur {user} par Pharmacie')
            plt.legend()
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()
        pass

    def generate_validation_rate_of_medicine_movements_by_pharmacy_chart(self, movements_data):
       # Exemple de graphique pour le taux de validation des mouvements de médicaments par pharmacie
        # Utilisez les données appropriées pour générer le graphique

        # Extracting data for the chart
        pharmacy_validation_data = {}  # Assuming movements_data is a list of objects with relevant attributes
        for movement in movements_data:
            pharmacy = movement.pharmacy_name
            is_validated = movement.is_validated  # Assuming there is an attribute indicating validation status

            if pharmacy not in pharmacy_validation_data:
                pharmacy_validation_data[pharmacy] = {'total': 0, 'validated': 0}

            pharmacy_validation_data[pharmacy]['total'] += 1
            if is_validated:
                pharmacy_validation_data[pharmacy]['validated'] += 1

        # Calculating validation rates
        validation_rates = {}
        for pharmacy, data in pharmacy_validation_data.items():
            total = data['total']
            validated = data['validated']
            rate = (validated / total) * 100 if total > 0 else 0
            validation_rates[pharmacy] = rate

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.bar(validation_rates.keys(), validation_rates.values(), color='green', alpha=0.7)

        plt.xlabel('Pharmacie')
        plt.ylabel('Taux de Validation (%)')
        plt.title('Taux de Validation des Mouvements de Médicaments par Pharmacie')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        pass

    def generate_total_cost_of_medicine_movements_by_period_pharmacy_chart(self, movements_data):
        # Exemple de graphique pour le coût total des mouvements de médicaments par période par pharmacie
        # Utilisez les données appropriées pour générer le graphique

        # Extracting data for the chart
        pharmacy_cost_data = {}  # Assuming movements_data is a list of objects with relevant attributes
        for movement in movements_data:
            pharmacy = movement.pharmacy_name
            cost = movement.medicine_cost  # Assuming there is an attribute indicating the cost

            if pharmacy not in pharmacy_cost_data:
                pharmacy_cost_data[pharmacy] = {'total_cost': 0}

            pharmacy_cost_data[pharmacy]['total_cost'] += cost

        # Plotting
        plt.figure(figsize=(12, 6))
        for pharmacy, data in pharmacy_cost_data.items():
            plt.bar(pharmacy, data['total_cost'], color='blue', alpha=0.7)

        plt.xlabel('Pharmacie')
        plt.ylabel('Coût Total des Mouvements de Médicaments')
        plt.title('Coût Total des Mouvements de Médicaments par Période par Pharmacie')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        pass

    def generate_medicine_movement_distribution_by_storage_location_pharmacy_chart(self, movements_data):
        # Exemple de graphique pour la répartition des mouvements de médicaments par emplacement de stockage par pharmacie
        # Utilisez les données appropriées pour générer le graphique

        # Extracting data for the chart
        pharmacy_storage_data = {}  # Assuming movements_data is a list of objects with relevant attributes
        for movement in movements_data:
            pharmacy = movement.pharmacy_name
            storage_location = movement.storage_location  # Assuming there is an attribute indicating the storage location

            if pharmacy not in pharmacy_storage_data:
                pharmacy_storage_data[pharmacy] = {'storage_locations': set()}

            pharmacy_storage_data[pharmacy]['storage_locations'].add(storage_location)

        # Plotting
        plt.figure(figsize=(12, 6))
        for pharmacy, data in pharmacy_storage_data.items():
            storage_count = len(data['storage_locations'])
            plt.bar(pharmacy, storage_count, color='green', alpha=0.7)

        plt.xlabel('Pharmacie')
        plt.ylabel('Nombre d\'Emplacements de Stockage')
        plt.title('Répartition des Mouvements de Médicaments par Emplacement de Stockage par Pharmacie')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        pass

    def generate_medicine_movement_distribution_by_storage_method_pharmacy_chart(self, movements_data):
        # Exemple de graphique pour la répartition des mouvements de médicaments par méthode de stockage par pharmacie
        # Utilisez les données appropriées pour générer le graphique

        # Extracting data for the chart
        pharmacy_method_data = {}  # Assuming movements_data is a list of objects with relevant attributes
        for movement in movements_data:
            pharmacy = movement.pharmacy_name
            storage_method = movement.storage_method  # Assuming there is an attribute indicating the storage method

            if pharmacy not in pharmacy_method_data:
                pharmacy_method_data[pharmacy] = {'storage_methods': set()}

            pharmacy_method_data[pharmacy]['storage_methods'].add(storage_method)

        # Plotting
        plt.figure(figsize=(12, 6))
        for pharmacy, data in pharmacy_method_data.items():
            method_count = len(data['storage_methods'])
            plt.bar(pharmacy, method_count, color='blue', alpha=0.7)

        plt.xlabel('Pharmacie')
        plt.ylabel('Nombre de Méthodes de Stockage')
        plt.title('Répartition des Mouvements de Médicaments par Méthode de Stockage par Pharmacie')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        pass

    def generate_expired_medicines_stock_by_pharmacy_chart(self, inventory_data):
        # Exemple de graphique pour le stock actuel des médicaments expirés par pharmacie
        # Utilisez les données appropriées pour générer le graphique

        # Extracting data for the chart
        pharmacy_expired_stock = {}  # Assuming inventory_data is a list of objects with relevant attributes
        for item in inventory_data:
            pharmacy = item.pharmacy_name
            expired_stock = item.expired_stock  # Assuming there is an attribute indicating the expired stock

            if pharmacy not in pharmacy_expired_stock:
                pharmacy_expired_stock[pharmacy] = {'expired_stock': 0}

            pharmacy_expired_stock[pharmacy]['expired_stock'] += expired_stock

        # Plotting
        plt.figure(figsize=(12, 6))
        for pharmacy, data in pharmacy_expired_stock.items():
            plt.bar(pharmacy, data['expired_stock'], color='red', alpha=0.7)

        plt.xlabel('Pharmacie')
        plt.ylabel('Stock de Médicaments Expirés')
        plt.title('Stock Actuel des Médicaments Expirés par Pharmacie')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        pass

    def generate_medicine_movement_distribution_by_lot_by_pharmacy_chart(self, movements_data):
        # Exemple de graphique pour la répartition des mouvements de médicaments par numéro de lot par pharmacie
        # Utilisez les données appropriées pour générer le graphique

        # Extracting data for the chart
        pharmacy_lot_distribution = defaultdict(lambda: defaultdict(int))

        for movement in movements_data:
            pharmacy = movement.pharmacy_name
            lot_number = movement.lot_number

            pharmacy_lot_distribution[pharmacy][lot_number] += 1

        # Plotting
        plt.figure(figsize=(12, 6))
        for pharmacy, lot_data in pharmacy_lot_distribution.items():
            lots = list(lot_data.keys())
            counts = list(lot_data.values())
            plt.bar(lots, counts, alpha=0.7, label=pharmacy)

        plt.xlabel('Numéro de Lot')
        plt.ylabel('Nombre de Mouvements')
        plt.title('Répartition des Mouvements de Médicaments par Numéro de Lot par Pharmacie')
        plt.legend()
        plt.tight_layout()
        plt.show()

        pass

    def generate_total_cost_of_medicine_movements_by_supplier_by_pharmacy_chart(self, movements_data):
        # Exemple de graphique pour le coût total des mouvements de médicaments par fournisseur par pharmacie
        # Utilisez les données appropriées pour générer le graphique

        # Extracting data for the chart
        pharmacy_supplier_cost = defaultdict(lambda: defaultdict(float))

        for movement in movements_data:
            pharmacy = movement.pharmacy_name
            supplier = movement.supplier_name
            cost = movement.cost

            pharmacy_supplier_cost[pharmacy][supplier] += cost

        # Plotting
        plt.figure(figsize=(12, 6))
        for pharmacy, supplier_data in pharmacy_supplier_cost.items():
            suppliers = list(supplier_data.keys())
            costs = list(supplier_data.values())
            plt.bar(suppliers, costs, alpha=0.7, label=pharmacy)

        plt.xlabel('Fournisseur')
        plt.ylabel('Coût Total des Mouvements')
        plt.title('Coût Total des Mouvements de Médicaments par Fournisseur par Pharmacie')
        plt.legend()
        plt.tight_layout()
        plt.show()
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

         

        # Ajouter les autres fonctions ici
        self.generate_article_quantity_by_category_chart(inventory_data)
        self.generate_current_stock_per_item_chart(inventory_data)
        self.generate_top_n_most_active_articles_chart(movements_data)
        self.generate_movement_distribution_by_type_chart(movements_data)
        self.generate_inventory_history_by_article_chart(movements_data)
        self.generate_top_n_most_active_medicines_chart(movements_data)
        self.generate_order_reception_evolution_chart(movements_data)
        self.generate_quantity_vs_minimum_by_article_chart(inventory_data)
        self.generate_supplier_distribution_by_product_chart(suppliers_data)
        self.generate_articles_without_replenishment_alerts_chart(inventory_data)
        self.generate_expired_medicines_stock_chart(inventory_data)
        self.generate_medicine_movement_distribution_by_lot_chart(movements_data)
        self.generate_total_cost_of_medicine_movements_by_supplier_chart(movements_data)
        self.generate_medicine_movement_distribution_by_pharmacy_chart(movements_data)
        self.generate_specific_medicine_stock_evolution_by_pharmacy_chart(movements_data)
        self.generate_replenishment_alert_distribution_by_pharmacy_chart(inventory_data)
        self.generate_quantity_vs_minimum_by_medicine_pharmacy_chart(inventory_data)
        self.generate_medicine_movement_distribution_by_user_pharmacy_chart(movements_data)
        self.generate_validation_rate_of_medicine_movements_by_pharmacy_chart(movements_data)
        self.generate_total_cost_of_medicine_movements_by_period_pharmacy_chart(movements_data)
        self.generate_medicine_movement_distribution_by_storage_location_pharmacy_chart(movements_data)
        self.generate_medicine_movement_distribution_by_storage_method_pharmacy_chart(movements_data)
        self.generate_expired_medicines_stock_by_pharmacy_chart(inventory_data)
        self.generate_medicine_movement_distribution_by_lot_by_pharmacy_chart(movements_data)
        self.generate_total_cost_of_medicine_movements_by_supplier_by_pharmacy_chart(movements_data)  


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
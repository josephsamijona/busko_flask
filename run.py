# run.py
from app import create_app, db
from app.models import *

app = create_app()

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cliniclelabo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de l'extension SQLAlchemy
db.init_app(app)

# Cette ligne crée les tables si elles n'existent pas encore
with app.app_context():
    # Crée les tables pour toutes les classes de modèle
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

# run.py
from app import create_app, db
from app.models import *
from flask_migrate import Migrate
from flask_migrate import upgrade, downgrade


app = create_app()

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cliniclelabo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de l'extension SQLAlchemy
db.init_app(app)
# Initialisation de l'extension Flask-Migrate
migrate = Migrate(app, db)
# Cette ligne crée les tables si elles n'existent pas encore
@app.cli.command('db_create')
def db_create():
    # Crée la base de données
    db.create_all()
    print('Database created!')

@app.cli.command('db_drop')
def db_drop():
    # Supprime la base de données
    db.drop_all()
    print('Database dropped!')

@app.cli.command('db_reset')
def db_reset():
    # Réinitialise la base de données (supprime et recrée)
    db.drop_all()
    db.create_all()
    print('Database reset!')

@app.cli.command('db_migrate')
def db_migrate():
    # Crée une nouvelle migration
    migrate.init()
    migrate.migrate()
    print('Migration created and applied!')

@app.cli.command('db_upgrade')
def db_upgrade():
    # Applique les migrations actuelles
    upgrade()
    print('Database upgraded!')

@app.cli.command('db_downgrade')
def db_downgrade():
    # Rejette la dernière migration
    downgrade()
    print('Database downgraded!')

    # Crée les tables pour toutes les classes de modèle
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

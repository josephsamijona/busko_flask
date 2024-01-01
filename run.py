# app/run.py
from app import create_app, db, login_manager

app = create_app()

# Initialisation de l'extension Flask-Login
login_manager.init_app(app)

# ... (le reste de votre code)

if __name__ == '__main__':
    app.run(debug=True)




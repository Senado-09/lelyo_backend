from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# 🔐 Charger les variables d’environnement depuis .env
load_dotenv()

# 📦 Lire l’URL PostgreSQL définie dans le fichier .env
DATABASE_URL = os.getenv("DATABASE_URL")

# 🌐 Créer l'engine pour PostgreSQL
engine = create_engine(DATABASE_URL)

# ⚙️ Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🧱 Base commune pour tous les modèles
Base = declarative_base()

# 🔁 Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

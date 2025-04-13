from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 🔧 Configuration MySQL (via WampServer)
DB_USERNAME = "root"           # par défaut avec Wamp
DB_PASSWORD = ""               # vide si tu n’as rien mis dans phpMyAdmin
DB_NAME = "ll_db"       # nom de ta base MySQL (à créer dans phpMyAdmin)
DB_HOST = "localhost"
DB_PORT = 3306

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 🌐 Créer l'engine pour MySQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

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

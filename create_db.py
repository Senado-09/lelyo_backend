from app.database import Base, engine, SessionLocal
from app.models.property import Property
from app.models.reservation import Reservation
from app.models.user import User

# Création des tables
Base.metadata.create_all(bind=engine)

# Ajouter un utilisateur test si non existant
db = SessionLocal()
existing = db.query(User).filter(User.email == "admin@host.com").first()
if not existing:
    user = User(email="admin@host.com", password="admin")
    db.add(user)
    print("Utilisateur 'admin@host.com' créé.")
else:
    print("Utilisateur déjà existant.")

db.commit()
db.close()

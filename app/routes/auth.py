
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.database import get_db, SessionLocal
from app.schemas.user import UserCreate
from app.utils.security import hash_password, verify_password 
from app.utils.jwt import create_access_token
from app.dependencies.auth import get_current_user


router = APIRouter()

 
@router.post("/login")
def login(data: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data["email"]).first()
    if not user or not verify_password(data["password"], user.password):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    token = create_access_token(data={"sub": user.email, "full_name": user.full_name})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Vérification email
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    # Vérification téléphone
    existing_phone = db.query(User).filter(User.phone == user_data.phone).first()
    if existing_phone:
        raise HTTPException(status_code=400, detail="Téléphone déjà utilisé")

    # Création utilisateur avec mot de passe haché
    new_user = User(
        full_name=user_data.full_name,
        phone=user_data.phone,
        email=user_data.email,
        password=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"success": True, "user_id": new_user.id}


@router.get("/me")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
    }

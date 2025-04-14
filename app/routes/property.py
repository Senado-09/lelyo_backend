from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.property import Property

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/properties")
def get_properties(request: Request, db: Session = Depends(get_db)):
    base_url = str(request.base_url).rstrip("/")
    props = db.query(Property).all()

    result = []
    for prop in props:
        image_url = prop.image_url
        if image_url and not image_url.startswith("http"):
            image_url = f"{base_url}/{image_url.lstrip('/')}"
        result.append({
            "id": prop.id,
            "name": prop.name,
            "address": prop.address,
            "description": prop.description,
            "image_url": image_url
        })
    return result

@router.post("/properties")
def create_property(data: dict, db: Session = Depends(get_db)):
    prop = Property(
        name=data.get("name"),
        address=data.get("address"),
        description=data.get("description"),
        image_url=data.get("image_url")
    )
    db.add(prop)
    db.commit()
    db.refresh(prop)
    return prop

@router.delete("/properties/{property_id}")
def delete_property(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(Property).get(property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Bien introuvable")
    db.delete(prop)
    db.commit()
    return {"success": True}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date
from app.database import SessionLocal
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationUpdate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/reservations")
def get_reservations(db: Session = Depends(get_db)):
    return db.query(Reservation).all()


@router.post("/reservations")
def create_reservation(data: dict, db: Session = Depends(get_db)):
    try:
        start = date.fromisoformat(data.get("start_date"))
        end = date.fromisoformat(data.get("end_date"))
        property_id = data.get("property_id")

        # Vérification de conflit
        conflict = db.query(Reservation).filter(
            Reservation.property_id == property_id,
            and_(
                Reservation.start_date <= end,
                Reservation.end_date >= start,
            )
        ).first()

        if conflict:
            raise HTTPException(
                status_code=409,
                detail="Une réservation existe déjà pour ces dates sur ce bien."
            )

        new_res = Reservation(
            guest_name=data.get("guest_name"),
            start_date=start,
            end_date=end,
            property_id=property_id,
        )
        db.add(new_res)
        db.commit()
        db.refresh(new_res)
        return new_res

    except Exception:
        raise HTTPException(status_code=400, detail="Erreur lors de la création")


@router.put("/reservations/{reservation_id}")
def update_reservation(reservation_id: int, data: ReservationUpdate, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Réservation non trouvée")

    # Vérification de conflit (sauf la réservation actuelle)
    conflict = db.query(Reservation).filter(
        Reservation.property_id == data.property_id,
        Reservation.id != reservation_id,
        and_(
            Reservation.start_date <= data.end_date,
            Reservation.end_date >= data.start_date,
        )
    ).first()

    if conflict:
        raise HTTPException(
            status_code=409,
            detail="Conflit avec une autre réservation sur ce bien"
        )

    reservation.guest_name = data.guest_name
    reservation.start_date = data.start_date
    reservation.end_date = data.end_date
    reservation.property_id = data.property_id

    db.commit()
    db.refresh(reservation)
    return reservation


@router.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Réservation non trouvée")

    db.delete(reservation)
    db.commit()
    return {"message": "Réservation supprimée"}

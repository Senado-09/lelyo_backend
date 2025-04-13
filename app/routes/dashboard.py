from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.database import SessionLocal
from app.models.property import Property
from app.models.reservation import Reservation
from app.models.task import Task

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/dashboard")
def dashboard_summary(db: Session = Depends(get_db)):
    today = date.today()

    total_properties = db.query(Property).count()
    today_reservations = db.query(Reservation).filter(
        Reservation.start_date <= today,
        Reservation.end_date >= today
    ).count()
    today_tasks = db.query(Task).filter(Task.date == today, Task.status != "terminée").count()

    return {
        "total_properties": total_properties,
        "today_reservations": today_reservations,
        "today_tasks": today_tasks,
    }

@router.get("/dashboard/reservations_week")
def reservations_last_7_days(property_id: int = Query(None), db: Session = Depends(get_db)):
    today = date.today()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]

    data = []
    for d in last_7_days:
        query = db.query(Reservation).filter(
            Reservation.start_date <= d,
            Reservation.end_date >= d
        )
        if property_id:
            query = query.filter(Reservation.property_id == property_id)

        count = query.count()
        data.append({"date": d.isoformat(), "count": count})

    return data

@router.get("/dashboard/alerts")
def get_alerts(db: Session = Depends(get_db)):
    today = date.today()
    tomorrow = today + timedelta(days=1)

    # Tâches en retard (avant aujourd’hui, non terminées)
    late_tasks = db.query(Task).filter(
        Task.date < today,
        Task.status != "terminée"
    ).all()

    # Réservations prévues demain
    tomorrow_reservations = db.query(Reservation).filter(
        Reservation.start_date == tomorrow
    ).all()

    return {
        "late_tasks": [
            {
                "id": task.id,
                "title": task.title,
                "date": task.date.isoformat(),
                "property_id": task.property_id,
            }
            for task in late_tasks
        ],
        "tomorrow_reservations": [
            {
                "id": res.id,
                "guest_name": res.guest_name,
                "start_date": res.start_date.isoformat(),
                "end_date": res.end_date.isoformat(),
                "property_id": res.property_id,
            }
            for res in tomorrow_reservations
        ],
    }
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.task import Task
from app.models.reservation import Reservation
from datetime import date, timedelta

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/stats")
def get_stats(property_id: int = Query(None), db: Session = Depends(get_db)):
    if property_id:
        total_reservations = db.query(Reservation).filter(Reservation.property_id == property_id).count()
        total_tasks = db.query(Task).filter(Task.property_id == property_id).count()
        done_tasks = db.query(Task).filter(Task.property_id == property_id, Task.status == "terminée").count()
    else:
        total_reservations = db.query(Reservation).count()
        total_tasks = db.query(Task).count()
        done_tasks = db.query(Task).filter(Task.status == "terminée").count()

    todo_tasks = total_tasks - done_tasks

    return {
        "reservations": total_reservations,
        "taches_total": total_tasks,
        "taches_terminees": done_tasks,
        "taches_a_faire": todo_tasks,
        "occupation_taux": f"{min(total_reservations * 10, 100)}%"
    }


@router.get("/stats/reservations_over_time")
def reservations_over_time(property_id: int = Query(None), db: Session = Depends(get_db)):
    today = date.today()
    last_30_days = [today - timedelta(days=i) for i in range(29, -1, -1)]

    results = []

    for d in last_30_days:
        query = db.query(Reservation).filter(
            Reservation.start_date <= d, Reservation.end_date >= d
        )
        if property_id:
            query = query.filter(Reservation.property_id == property_id)

        count = query.count()
        results.append({"date": d.isoformat(), "count": count})

    return results
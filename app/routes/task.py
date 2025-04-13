from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import SessionLocal
from app.models.task import Task

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


@router.get("/tasks/by_property/{property_id}")
def get_tasks_by_property(property_id: int, db: Session = Depends(get_db)):
    return db.query(Task).filter(Task.property_id == property_id).all()


@router.post("/tasks")
def create_task(data: dict, db: Session = Depends(get_db)):
    try:
        task = Task(
            title=data.get("title"),
            description=data.get("description"),
            date=date.fromisoformat(data.get("date")),
            status=data.get("status", "à faire"),
            property_id=data.get("property_id"),
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    except Exception as e:
        raise HTTPException(status_code=400, detail="Erreur lors de la création")
    
    
@router.patch("/tasks/{task_id}/toggle")
def toggle_task_status(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tâche introuvable")
    task.status = "terminée" if task.status != "terminée" else "à faire"
    db.commit()
    return {"status": task.status}


@router.put("/tasks/{task_id}")
def update_task(task_id: int, data: dict, db: Session = Depends(get_db)):
    task = db.query(Task).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tâche introuvable")

    try:
        task.title = data.get("title", task.title)
        task.description = data.get("description", task.description)
        task.date = date.fromisoformat(data.get("date")) if data.get("date") else task.date
        task.status = data.get("status", task.status)
        task.property_id = data.get("property_id", task.property_id)
        
        db.commit()
        db.refresh(task)
        return task
    except Exception:
        raise HTTPException(status_code=400, detail="Erreur lors de la mise à jour")


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tâche introuvable")
    db.delete(task)
    db.commit()
    return {"success": True}

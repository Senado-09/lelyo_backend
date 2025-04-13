from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(String(255))
    date = Column(Date)
    status = Column(String(255), default="à faire")  # ou "terminée"
    property_id = Column(Integer, ForeignKey("properties.id"))

# app/models/reservation.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.database import Base

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    guest_name = Column(String(255))
    start_date = Column(Date)
    end_date = Column(Date)
    property_id = Column(Integer, ForeignKey("properties.id"))

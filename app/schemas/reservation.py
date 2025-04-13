from pydantic import BaseModel
from datetime import date

class ReservationUpdate(BaseModel):
    guest_name: str
    start_date: date
    end_date: date
    property_id: int

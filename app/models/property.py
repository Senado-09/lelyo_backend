from sqlalchemy import Column, Integer, String
from app.database import Base

class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    address = Column(String(255))
    description = Column(String(255))
    image_url = Column(String(255), nullable=True)

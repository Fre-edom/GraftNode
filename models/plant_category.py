import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from database import Base


class PlantCategory(Base):
    __tablename__ = "plant_categories"

    category_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    category_name = Column(String, nullable=False)

    types = relationship("PlantType", back_populates="category")
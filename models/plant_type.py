import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class PlantType(Base):
    __tablename__ = "plant_types"

    type_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type_name = Column(String, nullable=False)
    id_category = Column(String, ForeignKey("plant_categories.category_id"))


    category = relationship("PlantCategory", back_populates="types")
    plants = relationship("Plant", back_populates="plant_type")
  
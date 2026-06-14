import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class PlantType(Base):
    __tablename__ = "plant_types"

    type_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type_name = Column(String, nullable=False)
    id_category = Column(String, ForeignKey("plant_categories.category_id"))

    # "one" side — this type belongs to one category
    category = relationship("PlantCategory", back_populates="types")
import uuid
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Plant(Base):
    __tablename__ = "plants"

    plant_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    id_user = Column(String, ForeignKey("users.user_id"))
    id_planttype = Column(String, ForeignKey("plant_types.type_id"))
    plant_petname = Column(String, nullable=True)
    plant_bio = Column(String, nullable=True)
    date_planted = Column(Date, nullable=True)
    soil_type = Column(String, nullable=True)
    notes = Column(String, nullable=True)

    user = relationship("User", back_populates="plants")
    plant_type = relationship("PlantType", back_populates="plants")
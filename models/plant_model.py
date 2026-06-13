from database import Base
from sqlalchemy import Column, Integer, String

class PlantModel(Base):
    __tablename__ = "plants"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=False)
    id_category = Column(String, index=True)
    id_type = Column(String, index=True)
    date_created = Column(String, index=False)

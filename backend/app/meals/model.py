# meals/model.py
from sqlalchemy import Column, Integer, String, Boolean, Text, Numeric, Enum as SQLEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from datetime import datetime

from config.database import Base

class CategoryEnum(SQLEnum):
    HAMBURGERS_AND_HOTDOGS = "HAMBURGERS_AND_HOTDOGS"
    CHICKEN = "CHICKEN"
    FISH = "FISH"
    MEATS = "MEATS"
    DESSERTS = "DESSERTS"
    VEGAN_FOOD = "VEGAN_FOOD"
    KIDS_MEALS = "KIDS_MEALS"

class Meal(Base):
    __tablename__ = "meals"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    category = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    price_without_iva = Column(Numeric(10, 2), nullable=False)
    is_available = Column(Boolean, default=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Meal(id={self.id}, uuid={self.uuid}, name='{self.name}', category='{self.category}')>"

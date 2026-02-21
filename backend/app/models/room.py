from sqlalchemy import Column, Integer, String, Float, Boolean, Text, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.core.database import Base
import enum

class RoomType(str, enum.Enum):
    STANDARD = "standard"
    DELUXE = "deluxe"
    SUITE = "suite"
    VILLA = "villa"

class RoomStatus(str, enum.Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    MAINTENANCE = "maintenance"

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String, unique=True, index=True, nullable=False)
    room_type = Column(SQLEnum(RoomType), nullable=False)
    status = Column(SQLEnum(RoomStatus), default=RoomStatus.AVAILABLE, nullable=False)
    price_per_night = Column(Float, nullable=False)
    capacity = Column(Integer, nullable=False)
    description_en = Column(Text, nullable=True)
    description_ar = Column(Text, nullable=True)
    amenities = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

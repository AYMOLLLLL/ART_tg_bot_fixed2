from sqlalchemy import String, Text, Numeric, DateTime, Boolean, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from utils.database import Base

class Schedule(Base):
    __tablename__ = "Schedule"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    section: Mapped[str] = mapped_column(String(100))
    time: Mapped[str] = mapped_column(String(100))
    free_place: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

class Promotion(Base):
    __tablename__ = "Promotion"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    text: Mapped[str] = mapped_column(String(1000))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
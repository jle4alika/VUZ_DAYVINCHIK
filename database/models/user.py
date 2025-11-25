"""
User database table
"""

import datetime
from sqlalchemy import func
from sqlalchemy import BigInteger, String, Float, Integer
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.orm import Mapped, mapped_column

from database.db import Base


class User(Base):
    """
    User table
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)

    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, default="", nullable=True)
    role: Mapped[str] = mapped_column(String, default="user", nullable=False)

    age: Mapped[int] = mapped_column(Integer, nullable=True)
    name: Mapped[str] = mapped_column(String, default="", nullable=True)
    phone_number: Mapped[str] = mapped_column(String(), nullable=True)
    about: Mapped[str] = mapped_column(String(), nullable=True)
    gender: Mapped[str] = mapped_column(String(10), nullable=True)  # "male", "female"
    looking_for: Mapped[str] = mapped_column(
        String(20), nullable=True
    )  # "male", "female", "any"

    city_name: Mapped[str] = mapped_column(String(200), nullable=True)  # Город руками
    latitude: Mapped[float] = mapped_column(
        Float, nullable=True
    )  # Координаты если отправили локацию
    longitude: Mapped[float] = mapped_column(Float, nullable=True)

    files: Mapped[str] = mapped_column(String, default="", nullable=False)

    last_activity: Mapped[datetime.datetime] = mapped_column(
        DATETIME, default=func.now()
    )
    registration_time: Mapped[datetime.datetime] = mapped_column(
        DATETIME, default=func.now()
    )

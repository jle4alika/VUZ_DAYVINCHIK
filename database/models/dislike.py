"""
Dislikes database table
"""

import datetime
from sqlalchemy import func
from sqlalchemy import BigInteger, String, Float
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.orm import Mapped, mapped_column

from database.db import Base


class Dislike(Base):
    """
    Dislike table
    """

    __tablename__ = "dislikes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    to_user_tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    created_time: Mapped[datetime.datetime] = mapped_column(
        DATETIME, default=func.now()
    )

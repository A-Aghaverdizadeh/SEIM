from __future__ import annotations
from datetime import datetime
from sqlalchemy import Boolean, String, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import UUIDMixin, TimestampMixin


class Agent(UUIDMixin, TimestampMixin, Base):
    """Represents a registered SIEM agent."""

    __tablename__ = "agents"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    hostname: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    api_key: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        index=True,
        nullable=False,
    )

    enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("true"),
    )

    events: Mapped[list["Event"]] = relationship(
        back_populates="agent",
        cascade="all, delete-orphan",
    )

    last_seen: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
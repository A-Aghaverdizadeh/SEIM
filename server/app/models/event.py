from __future__ import annotations
from datetime import datetime
from typing import Any

from sqlalchemy import ForeignKey, String, DateTime, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import UUIDMixin, TimestampMixin

class Event(UUIDMixin, TimestampMixin, Base):
    """Represents a normalized security event."""

    __tablename__ = "events"

    agent_id: Mapped[UUID] = mapped_column(
        ForeignKey("agents.id"),
        nullable=False,
        index=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    hostname: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    severity: Mapped[str] = mapped_column(
        String(25),
        nullable=False,
        index=True,
    )

    message: Mapped[str]

    attributes: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )

    agent: Mapped["Agent"] = relationship(
        back_populates="events"
    )
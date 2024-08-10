from datetime import datetime
from uuid import UUID
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as SQLAUUID
from sqlalchemy.orm import Mapped

from v1.clients.postgres import db


class User(db.Base):
    __tablename__ = "user_profiles"

    id: Mapped[UUID] = Column(SQLAUUID(as_uuid=True), primary_key=True)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    full_name: Mapped[str] = Column(String)
    username: Mapped[str] = Column(String)


class Resource(db.Base):
    __tablename__ = "lmdev_resources"

    id: Mapped[UUID] = Column(SQLAUUID(as_uuid=True), primary_key=True)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    title: Mapped[str] = Column(String)
    parent_id: Mapped[UUID] = Column(
        SQLAUUID(as_uuid=True), ForeignKey("lmdev_resources.id")
    )
    child_count: Mapped[int] = Column(Integer)
    slug: Mapped[str] = Column(String)
    author_id: Mapped[UUID] = Column(
        SQLAUUID(as_uuid=True), ForeignKey("user_profiles.id")
    )
    content: Mapped[str] = Column(String)
    list_order: Mapped[int] = Column(Integer)

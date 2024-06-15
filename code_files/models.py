from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID

import uuid

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    account_created = Column(DateTime(timezone=True), server_default=func.now())
    account_updated = Column(DateTime(timezone=True), onupdate=func.now())

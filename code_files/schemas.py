from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserCreate(BaseModel):
    username: EmailStr = Field(..., example="jane.doe@example.com")
    password: str = Field(..., example="skdjfhskdfjhg", write_only=True)
    first_name: str = Field(..., example="Jane")
    last_name: str = Field(..., example="Doe")

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, example="Jane")
    last_name: Optional[str] = Field(None, example="Doe")
    username: Optional[EmailStr] = Field(None, example="jane.doe@example.com")
    password: Optional[str] = Field(None, example="skdjfhskdfjhg", write_only=True)


class UserResponse(BaseModel):
    id: UUID = Field(..., example="d290f1ee-6c54-4b01-90e6-d701748f0851", read_only=True)
    email: EmailStr = Field(..., example="jane.doe@example.com")
    first_name: str = Field(..., example="Jane")
    last_name: str = Field(..., example="Doe")
    account_created: datetime = Field(..., example="2016-08-29T09:12:33.001Z", read_only=True)
    account_updated: Optional[datetime] = Field(None, example="2016-08-29T09:12:33.001Z", read_only=True)

    class Config:
        from_attributes = True

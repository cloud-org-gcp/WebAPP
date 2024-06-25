from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserCreate(BaseModel):
    username: EmailStr = Field(..., json_schema_extra={"example": "jane.doe@example.com"})
    password: str = Field(..., json_schema_extra={"example": "skdjfhskdfjhg", "writeOnly": True})
    first_name: str = Field(..., json_schema_extra={"example": "Jane"})
    last_name: str = Field(..., json_schema_extra={"example": "Doe"})

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, json_schema_extra={"example": "Jane"})
    last_name: Optional[str] = Field(None, json_schema_extra={"example": "Doe"})
    username: Optional[EmailStr] = Field(None, json_schema_extra={"example": "jane.doe@example.com"})
    password: Optional[str] = Field(None, json_schema_extra={"example": "skdjfhskdfjhg", "writeOnly": True})

class UserResponse(BaseModel):
    id: UUID = Field(..., json_schema_extra={"example": "d290f1ee-6c54-4b01-90e6-d701748f0851", "readOnly": True})
    email: EmailStr = Field(..., json_schema_extra={"example": "jane.doe@example.com"})
    first_name: str = Field(..., json_schema_extra={"example": "Jane"})
    last_name: str = Field(..., json_schema_extra={"example": "Doe"})
    account_created: datetime = Field(..., json_schema_extra={"example": "2016-08-29T09:12:33.001Z", "readOnly": True})
    account_updated: Optional[datetime] = Field(None, json_schema_extra={"example": "2016-08-29T09:12:33.001Z", "readOnly": True})
    model_config = {"from_attributes": True}

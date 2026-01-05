from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class TimestampMixin(BaseModel):
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 100
    
    class Config:
        json_schema_extra = {
            "example": {
                "skip": 0,
                "limit": 100
            }
        }


class PaginatedResponse(BaseModel):
    items: list
    total: int
    skip: int
    limit: int
    
    class Config:
        from_attributes = True

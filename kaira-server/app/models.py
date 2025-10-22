# app/models.py
from pydantic import BaseModel, Field, field_validator

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0)
    quantity: int = Field(default=1, ge=1)
  
    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('이름은 공백일 수 없습니다')
        return v.strip()


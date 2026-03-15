from core import logger
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict

# --- Schemas --- 
class UserCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(alias="fullName")
    age: int = Field(gt=18, lt=100)
    email: EmailStr
    salary: float 

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) < 3:
            logger.info(f"Validation failed for name: {value}")
            raise ValueError("Name too short")
        return value
 
class UserResponse(UserCreate):
    id: int
    name: str 
    email: str
    salary: float
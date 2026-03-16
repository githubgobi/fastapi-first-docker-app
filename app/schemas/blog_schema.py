from core import logger
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict

# --- Schemas ---
class BlogCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str
    content: str
    author_email: EmailStr

    @field_validator("title")
    def validate_title(cls, value):
        if len(value) < 5:
            logger.info(f"Validation failed for title: {value}")
            raise ValueError("Title too short")
        return value
    
class BlogResponse(BlogCreate):
    id: int
    title: str
    content: str
    author_email: str   
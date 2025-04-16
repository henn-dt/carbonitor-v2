from pydantic import BaseModel, EmailStr, Field

class CreateUserViewModel(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50, pattern="^[a-zA-Z0-9_-]+$")
    password: str = Field(min_length=8)
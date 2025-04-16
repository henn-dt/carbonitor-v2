from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

# Response models
class UserViewModel(BaseModel):
    id: int
    email: EmailStr
    username: str

class UserProfileViewModel(UserViewModel):
    is_verified: bool
    is_active: bool

class UserDetailViewModel(UserProfileViewModel):
    auth_method: str
    last_login_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

class UserListResponse(BaseModel):
    data: List[UserViewModel]

# Path parameter models
class UserPath(BaseModel):
    user_id: int
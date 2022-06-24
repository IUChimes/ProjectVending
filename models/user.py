from pydantic import BaseModel,validator
from fastapi import HTTPException, status

class User(BaseModel):
    username: str
    hashed_password: str
    role: str
    
    @validator("role")
    @classmethod
    def role_valid(cls, value):
        if value not in ["buyer","seller"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role must be either buyer or seller",
                headers={"WWW-Authenticate": "Bearer"},
            )        
        return value
    
class FullUser(User):
    id: str
    deposit: int

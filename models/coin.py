
from fastapi import HTTPException, status
from pydantic import BaseModel, validator

class Coin(BaseModel):
    value: int
    
    @validator("value")
    @classmethod
    def value_valid(cls, value):
        if value not in [5,10,20,50,100]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coin must have one of these values 5,10,20,50,100",
                headers={"WWW-Authenticate": "Bearer"},
            )        
        return value
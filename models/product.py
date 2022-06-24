from pydantic import BaseModel,validator
from fastapi import HTTPException, status

class Product(BaseModel):
    amountAvailable: int
    cost: int
    productName : str

class FullProduct(Product):
    sellerId: int
    sellerUsername: str
    rowID: int
    
class Purchase(BaseModel):
    amount: int
    rowID: int
    @validator("amount")
    @classmethod
    def amount_valid(cls, value):
        if value <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Purchase amount is incorrect",
                headers={"WWW-Authenticate": "Bearer"},
            )        
        return value
    
    @validator("rowID")        
    @classmethod
    def rowID_valid(cls, value):
        if value <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID value is incorrect",
                headers={"WWW-Authenticate": "Bearer"},
            )        
        return value
import database.database_connector as db_connector
from routers.auth import get_current_user
from fastapi import Depends, HTTPException, status, APIRouter
from models.coin import Coin
from models.product import Purchase
from models.user import User, FullUser

router = APIRouter(prefix="/api",tags=["vendor"])

def is_seller(user: User):
    return user.role == "seller"

@router.post("/deposit", status_code=200)
async def deposit(value: Coin, current_user: FullUser = Depends(get_current_user)):
    if(not is_seller(current_user)):
        await db_connector.add_coin(value,current_user)
    else:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Only buyers can deposit",
        headers={"WWW-Authenticate": "Bearer"},
    )     

@router.post("/reset", status_code=200)
async def deposit(current_user: FullUser = Depends(get_current_user)):
    if(not is_seller(current_user)):
        await db_connector.reset_deposit(current_user)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only buyers can reset deposit",
            headers={"WWW-Authenticate": "Bearer"},
        )   

def failed_purchase():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to purchase",
        headers={"WWW-Authenticate": "Bearer"},
    )   

def calculate_change(remainingChange: int, coinValue: int):
    if(remainingChange > 0 and remainingChange >= coinValue ):
        divisor = remainingChange // coinValue
        remainingChange -= divisor * coinValue
        return remainingChange, divisor
    return remainingChange,0

@router.post("/buy", status_code=200)
async def buy(purchase: Purchase,current_user: FullUser = Depends(get_current_user)):
    if(not is_seller(current_user)):
        product = await db_connector.fetch_product(purchase.rowID)
        if product and product.amountAvailable >= purchase.amount:
            totalPrice = purchase.amount * product.cost
            if(totalPrice <= current_user.deposit):
                remainingChange = current_user.deposit - totalPrice
                current_user.deposit = remainingChange
                await db_connector.modify_user_deposit(current_user)
                await db_connector.buy_product(purchase.amount, purchase.rowID)
                change = []
                for coin in (100,50,20,10,5):
                    remainingChange, divisor = calculate_change(remainingChange, coin)
                    change.extend([coin] * divisor)
                return {"Total": totalPrice, "Change": change}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient funds",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        failed_purchase()  
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only buyers can buy",
            headers={"WWW-Authenticate": "Bearer"},
        )   
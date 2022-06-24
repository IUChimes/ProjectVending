import database.database_connector as db_connector
from fastapi import Depends,APIRouter
from models.user import FullUser, User
from routers.auth import get_current_user

router = APIRouter(tags=["user"])

@router.get("/user", response_model=FullUser)
async def get_users(current_user: FullUser = Depends(get_current_user)):
    return current_user

@router.post("/user", status_code=201)
async def create_user(user: User):
    await db_connector.create_user(user)

@router.put("/user", status_code=200)
async def modify_user(user: User, current_user: FullUser = Depends(get_current_user)):
    await db_connector.modify_user(user,current_user.id)

@router.delete("/user", status_code=200)
async def delete_user(current_user: FullUser = Depends(get_current_user)):
    await db_connector.delete_user(current_user)
from databases import Database
from models.coin import Coin
from models.user import User, FullUser
from models.product import FullProduct, Product
from fastapi import HTTPException, status
from sqlite3 import IntegrityError

database = Database("sqlite:///vending.db")

async def fetch_user(username: str):
    query = "SELECT username, password, deposit, role, id FROM users WHERE username = :username"
    results = await database.fetch_one(query=query, values={"username": username })
    return results

async def create_user(user: User):
    query = "INSERT INTO users VALUES (NULL, :username , :password,0, :role);"
    try:
        results = await database.execute(query=query,values={"username": user.username ,"password": user.hashed_password, "role": user.role})
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must be Unique",
            headers={"WWW-Authenticate": "Bearer"},
        )   
    return results

async def modify_user(user: User, rowID: str):
    query = "UPDATE users SET username = :username , password = :password, role = :role where rowID = :rowID"
    results = await database.execute(query=query,values={"username": user.username ,"password": user.hashed_password,"role": user.role, "rowID": rowID})
    return results

async def delete_user(user: FullUser):
    query = "DELETE FROM users WHERE rowID = :rowID"
    results = await database.execute(query=query, values={"rowID": user.id})
    return results
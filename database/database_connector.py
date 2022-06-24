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


async def modify_user_deposit(user: FullUser):
    query = "UPDATE users SET deposit = :deposit where rowID = :rowID"
    results = await database.execute(query=query,values={"deposit": user.deposit , "rowID": user.id})
    return results

async def delete_user(user: FullUser):
    query = "DELETE FROM users WHERE rowID = :rowID"
    results = await database.execute(query=query, values={"rowID": user.id})
    return results

async def add_coin(coin: Coin, user:FullUser):
    query = "UPDATE users SET deposit = deposit + :deposit WHERE rowID = :rowID"
    results = await database.execute(query=query, values={"deposit": coin.value, "rowID": user.id})
    return results

async def reset_deposit(user:FullUser):
    query = "UPDATE users SET deposit = 0 WHERE rowID = :rowID"
    results = await database.execute(query=query, values={"rowID": user.id})
    return results

async def fetch_personal_products(current_user_ID: str):
    query = "SELECT amountAvailable, cost, productName, sellerID, users.username, products.rowID FROM products INNER JOIN users ON id = sellerID WHERE sellerID = :sellerID"
    results = await database.fetch_all(query=query,values={"sellerID": current_user_ID})
    return results

async def fetch_products():
    query = "SELECT amountAvailable, cost, productName, sellerID, users.username, products.rowID  FROM products INNER JOIN users ON id = sellerID"
    results = await database.fetch_all(query=query)
    return results

async def fetch_product(rowID: str):
    query = "SELECT amountAvailable, cost, productName, sellerID as sellerId, users.username as sellerUsername, products.rowID as rowID  FROM products INNER JOIN users ON id = sellerID where products.rowID = :rowID"
    results = await database.fetch_one(query=query,values={"rowID": rowID})
    return FullProduct(**results)

async def buy_product(amount: int, rowID: str):
    query = "UPDATE products SET amountAvailable = amountAvailable - :amount WHERE products.rowID = :rowID"
    results = await database.execute(query=query,values={"amount": amount, "rowID": rowID})
    return results

async def create_product(product: Product,current_user_ID: str):
    query = "INSERT INTO products VALUES (:amountAvailable , :cost ,:productName , :sellerID);"
    results = await database.execute(query=query,values={"amountAvailable": product.amountAvailable ,"cost": product.cost,"productName": product.productName, "sellerID": current_user_ID})
    return results

async def modify_product(product: Product, product_id: str,current_user_ID: str):
    query = "UPDATE products SET amountAvailable = :amountAvailable , cost = :cost , productName =:productName WHERE rowID = :rowID AND sellerID = :sellerID"
    results = await database.execute(query=query,values={"amountAvailable": product.amountAvailable ,"cost": product.cost,"productName": product.productName, "rowID": product_id, "sellerID": current_user_ID})
    return results

async def delete_product(product_id: str,current_user_ID: str):
    query = "DELETE FROM products WHERE rowID = :rowID AND sellerID = :sellerID"
    results = await database.execute(query=query,values={"rowID": product_id, "sellerID": current_user_ID})
    return results
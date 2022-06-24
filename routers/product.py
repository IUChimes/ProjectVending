import database.database_connector as db_connector
from fastapi import Depends, APIRouter
from models.product import Product,FullProduct
from models.user import FullUser
from routers.auth import get_current_user

router = APIRouter(prefix="/api/product",tags=["product"])

def merge_products(result):
    products = []
    for item in result:
        tempProduct = FullProduct(amountAvailable=item[0],cost=item[1],productName=item[2],sellerId=item[3],sellerUsername=item[4], rowID=item[5])
        products.append(tempProduct)
    return products

async def fetch_products():
    result = await db_connector.fetch_products()
    return merge_products(result)

async def fetch_personal_products(current_user: FullUser):
    result = await db_connector.fetch_personal_products(current_user.id)
    return merge_products(result)

@router.get("/", status_code=200)
async def get_products(current_user: FullUser = Depends(get_current_user)):
    result = await fetch_products()
    return { "products": result}

@router.get("/my", status_code=200)
async def get_products(current_user: FullUser = Depends(get_current_user)):
    result = await fetch_personal_products(current_user)
    return { "products": result}

@router.post("/my", status_code=201)
async def create_product(product: Product,current_user: FullUser = Depends(get_current_user)):
    result = await db_connector.create_product(product,current_user.id)
    return { "productID": result}

@router.put("/my/{product_id}", status_code=200)
async def modify_product(product_id: str,product: Product,current_user: FullUser = Depends(get_current_user)):
    await db_connector.modify_product(product,product_id,current_user.id)
    
@router.delete("/my/{product_id}", status_code=200)
async def delete_product(product_id: str,current_user: FullUser = Depends(get_current_user)):
    await db_connector.delete_product(product_id,current_user.id)

from fastapi.testclient import TestClient
import pytest

from main import app
from models.user import FullUser

client = TestClient(app)

buyer_access_token = ''
seller_access_token = ''

'''
Creates Users to continue tests with
'''
@pytest.mark.parametrize("username, role, resultStatus", [["TestBuyerUser", "buyer", 201], ["TestSellerUser", "seller", 201]])
def test_success_create_user(username, role, resultStatus):
    response = client.post("/user",headers={"Content-Type": "application/json"},json={
    "username":f"{username}",
    "hashed_password": "$2a$04$jROAfrQAhjRDHPmJCKwN4uyq33dPXxDrlYMy6UAvc8aEz/vUpQXTS",
    "role": f"{role}"
    })
    assert response.status_code == resultStatus

'''
Checks if role is buyer/seller enum
'''
def test_fail_role_create_user():
    response = client.post("/user",headers={"Content-Type": "application/json"},json={
    "username":"TestWrongUser",
    "hashed_password": "$2a$04$jROAfrQAhjRDHPmJCKwN4uyq33dPXxDrlYMy6UAvc8aEz/vUpQXTS",
    "role": "admin"
    })
    assert response.status_code == 400
    assert response.json()['detail']

'''
Checks if database allows duplicate usernames
'''
def test_fail_unique_create_user():
    response = client.post("/user",headers={"Content-Type": "application/json"},json={
    "username":"TestBuyerUser",
    "hashed_password": "$2a$04$jROAfrQAhjRDHPmJCKwN4uyq33dPXxDrlYMy6UAvc8aEz/vUpQXTS",
    "role": "buyer"
    })
    assert response.status_code == 400

'''
Login as buyer
'''
def test_buyer_login():
    response = client.post("/login",headers={"Content-Type": "application/x-www-form-urlencoded"},data={"username": "TestBuyerUser", "password": "newuserpassword"})
    global buyer_access_token 
    buyer_access_token = response.json()["access_token"]
    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["token_type"]
    
'''
Login as seller
'''
def test_seller_login():
    response = client.post("/login",headers={"Content-Type": "application/x-www-form-urlencoded"},data={"username": "TestSellerUser", "password": "newuserpassword"})
    global seller_access_token 
    seller_access_token = response.json()["access_token"]
    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["token_type"]
    
'''
Login exceptions
'''
@pytest.mark.parametrize("username, password, status", [["BadTestSellerUser","newuserpassword",401],["TestSellerUser","BADnewuserpassword",401]])
def test_fail_login(username,password, status):
    response = client.post("/login",headers={"Content-Type": "application/x-www-form-urlencoded"},data={"username": f"{username}", "password": f"{password}"})
    assert response.status_code == status
'''
Changes role to seller and reverts to buyer
'''
@pytest.mark.parametrize("role", [["seller"]])
def test_modify_user(role):    
    response = client.put("/user",headers={"Content-Type": "application/json","Authorization": f"Bearer {buyer_access_token}"},json={
    "username":"TestBuyerUser",
    "hashed_password": "$2a$04$jROAfrQAhjRDHPmJCKwN4uyq33dPXxDrlYMy6UAvc8aEz/vUpQXTS",
    "role": f"{role}"
    })
    assert response.status_code == 200
    response = client.put("/user",headers={"Content-Type": "application/json","Authorization": f"Bearer {buyer_access_token}"},json={
    "username":"TestBuyerUser",
    "hashed_password": "$2a$04$jROAfrQAhjRDHPmJCKwN4uyq33dPXxDrlYMy6UAvc8aEz/vUpQXTS",
    "role": "buyer"
    })
    
def test_info_user():
    response = client.get("/user",headers={"Authorization": f"Bearer {buyer_access_token}"})
    user = FullUser(**response.json())
    assert user.username == "TestBuyerUser"
    assert user.hashed_password == "$2a$04$jROAfrQAhjRDHPmJCKwN4uyq33dPXxDrlYMy6UAvc8aEz/vUpQXTS"
    assert user.deposit == 0
    assert user.role == "buyer"
    assert response.status_code == 200
    
'''
Changes role from seller to buyer
'''
def test_modify_user():    
    response = client.put("/user",headers={"Content-Type": "application/json","Authorization": f"Bearer {buyer_access_token}"},json={
    "username":"TestBuyerUser",
    "hashed_password": "$2a$04$jROAfrQAhjRDHPmJCKwN4uyq33dPXxDrlYMy6UAvc8aEz/vUpQXTS",
    "role": "buyer"
    })
    assert response.status_code == 200

'''
Deposit
'''
@pytest.mark.parametrize("coin, deposit, status", [[5,5,200],[5,10,200],[10,20,200],[20,40,200],[50,90,200],[100,190,200],[5,195,200],[10,205,200],[-1,205,400]])
def test_deposit(coin, deposit, status):
    response = client.post("/deposit",headers={"Content-Type": "application/json","Authorization": f"Bearer {buyer_access_token}"},json={"value":f"{coin}"})
    assert response.status_code == status
    response = client.get("/user",headers={"Authorization": f"Bearer {buyer_access_token}"})
    user = FullUser(**response.json())
    assert user.deposit == deposit  
    
'''
Deposit
'''
@pytest.mark.parametrize("coin, status", [[5,400],[5,400],[10,400],[20,400],[50,400],[100,400],[5,400],[10,400],[-1,400]])
def test_fail_deposit(coin, status):
    response = client.post("/deposit",headers={"Content-Type": "application/json","Authorization": f"Bearer {seller_access_token}"},json={"value":f"{coin}"})
    assert response.status_code == status
    
@pytest.mark.parametrize("amount, rowID, total, change, deposit", [[3,3,15, [100,50,20,20],190],[12,3,60, [100,20,10],130],[26,3,130, [],0]])
def test_success_buy(amount, rowID, total, change, deposit):
    response = client.post("/buy",headers={"Authorization": f"Bearer {buyer_access_token}"},json={"amount":f'{amount}', "rowID":f'{rowID}'})
    assert response.json()["Total"] == total   
    assert response.json()["Change"] == change   
    assert response.status_code == 200   
    response = client.get("/user",headers={"Authorization": f"Bearer {buyer_access_token}"})
    user = FullUser(**response.json())
    assert user.deposit == deposit  
    
@pytest.mark.parametrize("amount, rowID", [[3,3],[12,3],[-1000,1]])
def test_fail_buyer_buy(amount, rowID):
    response = client.post("/buy",headers={"Authorization": f"Bearer {buyer_access_token}"},json={"amount":f'{amount}', "rowID":f'{rowID}'})
    assert response.status_code == 400
    
@pytest.mark.parametrize("amount, rowID", [[3,3],[12,3],[-1000,1]])
def test_fail_seller_buy(amount, rowID):
    response = client.post("/buy",headers={"Authorization": f"Bearer {seller_access_token}"},json={"amount":f'{amount}', "rowID":f'{rowID}'})
    assert response.status_code == 400
    
def test_success_reset_deposit():
    response = client.post("/reset",headers={"Authorization": f"Bearer {buyer_access_token}"})
    assert response.status_code == 200
    response = client.get("/user",headers={"Authorization": f"Bearer {buyer_access_token}"})
    user = FullUser(**response.json())
    assert user.deposit == 0  
    
def test_fail_reset_deposit():
    response = client.post("/reset",headers={"Authorization": f"Bearer {seller_access_token}"})
    assert response.status_code == 400    
'''
Delete Test Buyer
'''
def test_delete_buyer_user():
    response = client.delete("/user",headers={"Authorization": f"Bearer {buyer_access_token}"})
    assert response.status_code == 200
    
'''
Delete Test Seller
'''
def test_delete_seller_user():
    response = client.delete("/user",headers={"Authorization": f"Bearer {seller_access_token}"})
    assert response.status_code == 200
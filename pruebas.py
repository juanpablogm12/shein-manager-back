
from passlib.context import CryptContext 
from db.client import db_client
from db.client import db_client
from db.models.user import User
# from typing import Annotated
# from pydantic import BaseModel
from db.schemas.user import user_schema



from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(username: str):
    return db_client.shein_manager.users.find_one({"username": username})

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.get("password")):
        return False
    return user



def login(username, password):
    user =authenticate_user(username, password)
    if not user:
        return "credenciales incorrectas"
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.get("username")}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


prueba = login("juan@hotmail.com", "1234")

print(prueba)
# print(db_client.shein_manager.users.find)

# password = "1238"

# crypt = CryptContext(schemes=["bcrypt"])

# password_hash = crypt.hash(password)

# prueba = crypt.verify("1234", password_hash)

# print(prueba)



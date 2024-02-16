from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext 
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "sfds1f65FDFD1561s6fsdFSDFe54f5"

router = APIRouter(prefix="/users")

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "juan": {
        "username": "juan",
        "full_name": "juan pablo",
        "email": "juan@gmail.com",
        "disabled": False,
        "password": "$2a$12$U67B4s3xRHaiMCiF0Kfone/BKlbFRr62/vso.lkgbCe4UVQlM.cJ6"
    },
    "jose": {
        "username": "jose",
        "full_name": "jose pablo",
        "email": "jose@gmail.com",
        "disabled": True,
        "password": "$2a$12$t3Bck.C5l3rngW3BO3PNTuHfPhKKG/FGEGFRuQCkCzwAkDs5daS32"
    },
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    

async def auth_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación invalidas",
        headers={"WWW-Authenticate": "Bearer"})   

    try: 
        username = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception
    
    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )

    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=400, detail="el usuario no es correcto"
        )
    user = search_user_db(form.username)

    

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=400, detail="la contraseña no es correcta"
        )

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)

    access_token = {
        "sub" : user.username,
        "exp": expire,
    }

    return {"acces_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@router.get("/me")
async def me(user: User = Depends(current_user)):
    return user

# from fastapi import APIRouter, Depends, HTTPException, status
# from pydantic import BaseModel
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# router = APIRouter(prefix="/users")

# oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# class User(BaseModel):
#     username: str
#     full_name: str
#     email: str
#     disabled: bool

# class UserDB(User):
#     password: str

# users_db = {
#     "juan": {
#         "username": "juan",
#         "full_name": "juan pablo",
#         "email": "juan@gmail.com",
#         "disabled": False,
#         "password": "1234"
#     },
#     "jose": {
#         "username": "jose",
#         "full_name": "jose pablo",
#         "email": "jose@gmail.com",
#         "disabled": True,
#         "password": "45678"
#     },
# }

# def search_user_db(username: str):
#     if username in users_db:
#         return UserDB(**users_db[username])

# def search_user(username: str):
#     if username in users_db:
#         return User(**users_db[username])
    

# async def current_user(token: str = Depends(oauth2)):
#     user = search_user(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Credenciales de autenticación invalidas",
#             headers={"WWW-Authenticate": "Bearer"}
#         )
#     if user.disabled:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Usuario inactivo"
#         )

#     return user
    
# @router.post("/login")
# async def login(form: OAuth2PasswordRequestForm = Depends()):
#     user_db = users_db.get(form.username)
#     if not user_db:
#         raise HTTPException(
#             status_code=400, detail="el usuario no es correcto"
#         )
#     user = search_user_db(form.username)
#     if not form.password == user.password:
#         raise HTTPException(
#             status_code=400, detail="la contraseña no es correcta"
#         )
#     return {"acces_token": user.username, "token_type": "bearer"}

# @router.get("/me")
# async def me(user: User = Depends(current_user)):
#     return user



# from fastapi import APIRouter
# from pydantic import BaseModel

# router = APIRouter()

# class User(BaseModel):
#     id: int
#     name: str
#     surname: str
#     url: str
#     age: int


# users_lists = [User(id=1,name="pablo",surname="guzman",url="https://pablo.com",age=27),
#                User(id=2,name="andrea",surname="flores",url="https://andrea.com",age=22),
#                User(id=3,name="juliana",surname="yarcer",url="https://juliana.com",age=25)]

# @router.get("/users")
# async def users():
#     return users_lists

# @router.get("/user/{id}")
# async def user(id: int):
#     search_user(id)
    
# @router.post("/user")
# async def user(user: User): 
#     if type(search_user(user.id)) == User:
#         return {"error" : "El Usuario ya existe"}
#     else: users_lists.append(user)


# def search_user(id: int):
#     users = filter(lambda user: user.id == id, users_lists)
#     try:
#         return list(users)[0]
#     except:
#         return {"error": "no se ha encontrado el usuario"}
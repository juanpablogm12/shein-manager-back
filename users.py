from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_lists = [User(id=1,name="pablo",surname="guzman",url="https://pablo.com",age=27),
               User(id=2,name="andrea",surname="flores",url="https://andrea.com",age=22),
               User(id=3,name="juliana",surname="yarcer",url="https://juliana.com",age=25)]

@app.get("/users")
async def users():
    return users_lists

@app.get("/user/{id}")
async def user(id: int):
    search_user(id)
    
@app.post("/user")
async def user(user: User): 
    if type(search_user(user.id)) == User:
        return {"error" : "El Usuario ya existe"}
    else: users_lists.append(user)


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_lists)
    try:
        return list(users)[0]
    except:
        return {"error": "no se ha encontrado el usuario"}
from fastapi import FastAPI
from routers import users, scraping_products
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(scraping_products.router, prefix="/scraping_products", tags=["scraping_products"])

@app.get("/")
def root():
    return "hello world"
from pydantic import BaseModel


class User(BaseModel):
    id: str | None = None
    username: str
    first_name: str
    last_name: str
    session_id: str | None = None
    disabled: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserInDB(User):
    password: str
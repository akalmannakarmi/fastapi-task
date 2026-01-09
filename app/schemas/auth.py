from pydantic import BaseModel, EmailStr


class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str
    password2: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class UserLogout(BaseModel):
    refresh_token: str


class UserRefresh(BaseModel):
    refresh_token: str

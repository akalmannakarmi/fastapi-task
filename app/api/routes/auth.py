from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.db.crud import get_user_by_email, create_user, delete_refresh_token
from app.api.deps import get_db,get_current_user
from app.core.security import verify_password
from app.schemas.auth import UserSignup, UserLogin, UserOut, TokenOut
from app.utils.auth import create_tokens, get_access_token
from app.db.models import User

router = APIRouter()

@router.post("/signup",response_model=UserOut,status_code=201)
def signup(user:UserSignup, db:Session= Depends(get_db)):
    existing_user = get_user_by_email(db,user.email)
    if existing_user:
        return HTTPException(400,"An Account with the email already exists.")
    
    if user.password != user.password2:
        return HTTPException(400,"Passwords dont match")
    
    try:
        user = create_user(db,user.username,user.email,user.password)
    except Exception as e:
        print("Failed to create user",e.with_traceback())
        return HTTPException(500,"Failed to create user")
    
    return user

@router.post("/login",response_model=TokenOut)
def login(user:UserLogin, db:Session= Depends(get_db)):
    existing_user = get_user_by_email(db,user.email)

    if not user or not verify_password(user.password,existing_user.hashed_password):
        return HTTPException(401,"Invalid Credentials")
    
    access_token, refresh_token = create_tokens(db,existing_user.id)

    return {"access_token":access_token, "refresh_token":refresh_token , "token_type": "bearer"}


@router.post("/logout")
def logout(refresh_token:str, user:User = Depends(get_current_user), db:Session= Depends(get_db)):
    delete_refresh_token(db,refresh_token,user.id)

    return {"detail":"Logout successfull"}


@router.post("/refresh",response_model=TokenOut)
def refresh(refresh_token:str, db:Session= Depends(get_db)):
    access_token = get_access_token(db,refresh_token)

    return {"access_token":access_token,"refresh_token":refresh_token,"token_type":"bearer"}


@router.get("/me",response_model=UserOut)
def refresh(user:User = Depends(get_current_user)):
    return user
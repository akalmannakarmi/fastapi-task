from app.db.database import SessionLocal
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime,timezone
from app.db.models import User

oauth_schema = OAuth2PasswordBearer("/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    token:str = Depends(oauth_schema),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(token)

        user_id:str|None = payload.get("sub")
        expire_at:datetime|None = payload.get("exp")
        if not user_id or not expire_at:
            raise HTTPException(400,"Invalid Token")
        
        if expire_at < datetime.now(timezone.utc):
            raise HTTPException(400,"Token has expired")
    except JWTError:
        raise HTTPException(400,"Invalid Token")
    
    user = db.query(User).get(user_id)

    if not user:
        raise HTTPException(404,"User Not Found")
    
    return user

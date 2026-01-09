from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.security import create_access_token, create_refresh_token
from app.db.models import RefreshToken


def create_tokens(db: Session, userId: int):
    access_token = create_access_token({"type": "access", "sub": str(userId)})
    refresh_token = create_refresh_token({"type": "refresh", "sub": str(userId)})

    ref_token = RefreshToken(
        token=refresh_token,
        user_id=userId,
    )
    db.add(ref_token)
    db.commit()

    return access_token, refresh_token


def get_access_token(db: Session, refresh_token: str):
    ref_token = db.query(RefreshToken).get(refresh_token)
    if not ref_token:
        raise HTTPException(404, "token not found")

    access_token = create_access_token(
        {"type": "access", "sub": str(ref_token.user_id)}
    )
    return access_token

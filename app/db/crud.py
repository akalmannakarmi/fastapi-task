from sqlalchemy.orm import Session
from app.db import models
from app.core.security import hash_password


def create_user(db: Session, username: str, email: str, password: str) -> models.User:
    user = models.User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()


def delete_refresh_token(db: Session, refresh_token: str, userId: int):
    instance = db.query(models.RefreshToken).get(refresh_token)
    if instance and instance.user_id == userId:
        db.delete(instance)
        db.commit()

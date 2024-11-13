from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import models, crud
from database.database import SessionLocal, engine

authen = APIRouter()

# Tạo tất cả các bảng trong CSDL
models.Base.metadata.create_all(bind=engine)

# Dependency for getting DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@authen.get("/auth/{email}")
def read_user(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_email(db, email=email)
    if db_user is None:
        return {
            "status": False
        }
    return {
        "status": True,
    }
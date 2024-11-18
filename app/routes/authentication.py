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
    
    reg = crud.get_status(db, email=email)

    return {
        "status": True,
        "reg": reg
    }


@authen.post("/update-reg/{email}")
def update_reg(email: str, db: Session = Depends(get_db)):
    updated_user = crud.update_registration_status(db, email=email, status=1)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "status": True,
        "message": "Registration status updated successfully",
        "user": {
            "email": updated_user.email,
            "reg": updated_user.reg
        }
    }

@authen.post("/reset-reg/{email}")
def update_reg(email: str, db: Session = Depends(get_db)):
    updated_user = crud.update_registration_reset(db, email=email, status=0)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "status": True,
        "message": "Reset Registration status updated successfully",
        "user": {
            "email": updated_user.email,
            "reg": updated_user.reg
        }
    }
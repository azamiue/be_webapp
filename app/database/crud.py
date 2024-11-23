from sqlalchemy.orm import Session
from . import models


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_status(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first().reg

def update_registration_status(db: Session, email: str, status: int = 1):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        db_user.reg = status
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def update_registration_reset(db: Session, email: str, status: int = 0):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        db_user.reg = status
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def update_registration_le_status(db: Session, email: str, status: int = 1):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        db_user.le = status
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def update_registration_le_reset(db: Session, email: str, status: int = 0):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        db_user.le = status
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def update_registration_hoi_status(db: Session, email: str, status: int = 1):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        db_user.hoi = status
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def update_registration_hoi_reset(db: Session, email: str, status: int = 0):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        db_user.hoi = status
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def update_registration_cahai_status(db: Session, email: str, status: int = 1):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        db_user.cahai = status
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def update_registration_cahai_reset(db: Session, email: str, status: int = 0):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        db_user.cahai = status
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def create_user(db: Session, name: str, email: str):
    db_user = models.User(name=name, email=email, reg=False, le=False, hoi=False, cahai=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
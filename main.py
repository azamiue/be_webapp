from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, crud
from .database import SessionLocal, engine

# Tạo tất cả các bảng trong CSDL
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Vercel app     URL
    allow_credentials=True,
    allow_methods=["*"],  # You can specify methods like ['GET', 'POST'] if needed
    allow_headers=["*"],  # You can specify headers like ['Content-Type', 'Authorization'] if needed
)

# Dependency để lấy session database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    return crud.create_user(db=db, name=name, email=email)

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/auth/email/{email}")
def read_gmail(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_gmail(db, email = email)
    if db_user is None:
       return {
           "status": False
       }
    return {
        "status": True,
    }




from fastapi import FastAPI
from middleware import CORSMiddleware, LogProcessAndTime
from routes.collectdata import router
from routes.authentication import authen
from routes.createUser import users
from routes.email_routes import email_routes
from routes.zip_file import zip_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LogProcessAndTime)
app.include_router(router)
app.include_router(authen)
app.include_router(users)
app.include_router(email_routes, prefix="/api/v1")
app.include_router(zip_router)
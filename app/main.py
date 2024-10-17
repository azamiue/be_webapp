from fastapi import FastAPI
from middleware import CORSMiddleware, LogProcessAndTime
from routes.collectdata import router 

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


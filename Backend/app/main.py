from fastapi import FastAPI
from dotenv import load_dotenv
from app.database.database import Base,engine
from app.routing.endpoints import router
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()



Base.metadata.create_all(bind = engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,   # 🔴 REQUIRED for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"message":"fastapi working"}

app.include_router(router)
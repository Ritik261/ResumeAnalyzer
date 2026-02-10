from fastapi import FastAPI
from app.database.database import Base,engine
from app.routing.endpoints import router



Base.metadata.create_all(bind = engine)
app = FastAPI()

@app.get("/")
def health():
    return {"message":"fastapi working"}

app.include_router(router)
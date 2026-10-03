import uvicorn
from fastapi import FastAPI
from app.routers.key_route import router as key_router
from app.routers.well_known_route import router as discovery_router

app = FastAPI()

app.include_router(key_router)
app.include_router(discovery_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
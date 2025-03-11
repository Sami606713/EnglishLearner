from fastapi import FastAPI
from routers.textRoutes import routes as textRoutes

app = FastAPI()

app.include_router(textRoutes)

app.get("/")
def home():
    return "Welcome to the text correction API"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0")
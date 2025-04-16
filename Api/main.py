from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.textRoutes import routes as textRoutes

app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],          # Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],          # Allow all headers
)

app.include_router(textRoutes)

@app.get("/")  # Fixed missing decorator '@'
def home():
    return {"message": "Welcome to the text correction API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

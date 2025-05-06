from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, categories, prompts, auth

app = FastAPI(
    title="Test Application",
    description="Role-based API with User and Category Management",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(prompts.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Test Application"}

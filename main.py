from fastapi import FastAPI
from database import Base, engine
import models
from routes import router
from fastapi.middleware.cors import CORSMiddleware


# Create all database tables if they don't exist
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app instance
app = FastAPI()
app.include_router(router)


# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,  # Allow credentials (cookies, authorization headers)
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
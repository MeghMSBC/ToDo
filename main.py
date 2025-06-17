from fastapi import FastAPI
import models 
import database
from routes import router
app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)

app.include_router(router)
from fastapi import FastAPI
from app.api.routes import customer, auth

app = FastAPI()

app.include_router(customer.router, prefix="/customers", tags=["customers"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

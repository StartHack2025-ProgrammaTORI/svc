from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

from svc.plugin.consultant import controller as consultant_controller
from svc.plugin.company import controller as company_controller

app = FastAPI(version=os.environ["VERSION"])  # Added version prefix

app.include_router(consultant_controller.router)
app.include_router(company_controller.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the FastAPI application!",
        "environment": os.getenv("ENVIRONMENT", "development")  # Example usage of an env variable
    }

from fastapi import FastAPI
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from svc.plugin.consultant import controller as consultant_controller
from svc.plugin.question import controller as question_controller
from svc.plugin.todo import controller as todo_controller

app = FastAPI(version=os.environ["VERSION"])  # Added version prefix

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(consultant_controller.router)
app.include_router(question_controller.router)
app.include_router(todo_controller.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the FastAPI application!",
        "environment": os.getenv("ENVIRONMENT", "development")  # Example usage of an env variable
    }

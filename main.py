from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
import os
from svc.utils.firebase import initialize_firebase
initialize_firebase()
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from svc.utils.dataset import read_csv
from svc.utils.database import mongo_client
from svc.plugin.consultant import controller as consultant_controller
from svc.plugin.question import controller as question_controller
from svc.plugin.todo import controller as todo_controller
from svc.plugin.recomendation import controller as recommendation_controller

app = FastAPI(version=os.environ["VERSION"])  # Added version prefix

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    try:
        # Test MongoDB connection
        mongo_client.admin.command('ping')
        print("Connected to MongoDB successfully!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    mongo_client.close()
    print("MongoDB connection closed.")

app.include_router(consultant_controller.router)
app.include_router(question_controller.router)
app.include_router(todo_controller.router)
app.include_router(recommendation_controller.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the FastAPI application!",
        "environment": os.getenv("ENVIRONMENT", "development")  # Example usage of an env variable
    }

# @app.get("/test")
# def get_users():
#     """
#     Fetch all documents from the User collection.
#     """
#     try:
#         csv_ = read_csv(os.environ["DB"])
#         print("csv_", csv_.to_dict(orient="records"))
#         db.company.insert_many(csv_.to_dict(orient="records"))
#         users = list(db["User"].find({}, {"_id": 0}))  # Exclude the _id field from the response
#         return {"users": users}
#     except Exception as e:
#         return {"error": str(e)}

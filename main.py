from dotenv import load_dotenv
load_dotenv()

from svc.utils.database import db
from fastapi import FastAPI
import os
from svc.utils.firebase import initialize_firebase
initialize_firebase()
from fastapi.middleware.cors import CORSMiddleware
from svc.utils.database import mongo_client
from svc.plugin.consultant import controller as consultant_controller
from svc.plugin.question import controller as question_controller
from svc.plugin.todo import controller as todo_controller
from svc.plugin.proposal import controller as recommendation_controller
from svc.utils.model import Model

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

# model = Model()

# @app.get("/func")
# def create_embeddings():
#     try:
#         for company in db.company.find():
#             # Add description_embedded only if it doesn't exist
#             description = model.text_to_embedding(company['description'])
#             db.company.update_one(
#                 {"_id": company["_id"], "description_embedded": {"$exists": False}},
#                 {"$set": {"description_embedded": description}}
#             )
#     except Exception as e:
#         return {"error": str(e)}

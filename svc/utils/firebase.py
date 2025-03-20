import firebase_admin
from firebase_admin import credentials
import os

# Initialize Firebase with the service account file
def initialize_firebase():
    service_account_path = os.path.join(os.getcwd(), 'svc/utils/service_account.json')
    if not os.path.exists(service_account_path):
        raise FileNotFoundError(f"Service account file not found at: {service_account_path}")
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred)


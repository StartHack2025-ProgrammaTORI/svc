
from fastapi import HTTPException, Request
from firebase_admin import auth

async def validate_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization token is missing or invalid")
    token = auth_header.split(" ")[1]
    try:
        decoded_token = auth.verify_id_token(token)
        request.state.user = decoded_token  # Attach user info to the request state
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

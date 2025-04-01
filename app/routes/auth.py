from fastapi import APIRouter, HTTPException
from app.schemas.auth_schema import LoginRequest
from app.services.auth_service import get_token
from app.models.token import Token
from fastapi import Depends
import requests
from app.utils.keycloak import verify_token, check_user_role, oauth2_scheme
from starlette.responses import JSONResponse
from app.config import settings
from pydantic import BaseModel


router = APIRouter()

class LogoutRequest(BaseModel):
    refresh_token: str  # Expect refresh token in the request body

# login end_point
@router.post("/login", response_model=Token)
async def login(login_request: LoginRequest):
    try:
        token = await get_token(login_request.username, login_request.password)
        return token
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))



# logout end_point
@router.post("/logout", summary="Logout user from Keycloak")
async def logout(data: LogoutRequest):
    """
    Logout user by calling Keycloak's logout endpoint.
    """
    logout_url = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/logout"

    payload = {
        "client_id": settings.KEYCLOAK_CLIENT_ID,
        "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
        "refresh_token": data.refresh_token,  # Get refresh token from request body
    }

    response = requests.post(logout_url, data=payload)

    if response.status_code == 200:
        return {"message": "Successfully logged out"}

    # Print the exact error message for debugging
    error_message = response.text
    print(f"Keycloak logout error: {error_message}")

    raise HTTPException(
        status_code=response.status_code,
        detail=f"Logout failed: {error_message}"
    )


# admin route
@router.get("/admin", dependencies=[Depends(verify_token)])
async def admin_route(token: str = Depends(oauth2_scheme)):
    # Check if user has the admin role
    await check_user_role(token, ["admin"])
    return {"message": "Welcome, Admin!"}
# student route 
@router.get("/student", dependencies=[Depends(verify_token)])
async def student_route(token: str = Depends(oauth2_scheme)):
    # Check if user has the student role
    await check_user_role(token, ["student"])
    return {"message": "Welcome, Student!"}
# teacher route
@router.get("/teacher", dependencies=[Depends(verify_token)])
async def teacher_route(token: str = Depends(oauth2_scheme)):
    # Check if user has the teacher role
    await check_user_role(token, ["Teacher"])
    return {"message": "Welcome, Teacher!"}

@router.get("/protected", dependencies=[Depends(verify_token)])
async def protected_route():
    return {"message": "You have access to this protected route!"}
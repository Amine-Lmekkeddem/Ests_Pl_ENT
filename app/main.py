from app.routes import auth
from fastapi import FastAPI
app = FastAPI()

app.include_router(auth.router, prefix="/auth")

@app.get("/")
async def root():
    return {"message": "Welcome to the Authentication Microservice"}
from app.config import settings

print("KEYCLOAK_URL:", settings.KEYCLOAK_URL)
print("KEYCLOAK_REALM:", settings.KEYCLOAK_REALM)
print("KEYCLOAK_CLIENT_ID:", settings.KEYCLOAK_CLIENT_ID)
print("KEYCLOAK_CLIENT_SECRET:", settings.KEYCLOAK_CLIENT_SECRET)

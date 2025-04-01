import httpx
from app.config import settings
from app.models.token import Token

async def get_token(username: str, password: str) -> Token:
    token_url = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"
    data = {
        "client_id": settings.KEYCLOAK_CLIENT_ID,
        "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
        "grant_type": "password",
        "username": username,
        "password": password,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)

        if response.status_code != 200:
            raise Exception("Invalid credentials or Keycloak error")
        print(response.json())
        token_data = response.json()
        return Token(
            access_token=token_data["access_token"],
            token_type=token_data["token_type"],
            expires_in=token_data["expires_in"],
            refresh_token=token_data.get("refresh_token"),
            refresh_expires_in=token_data.get("refresh_expires_in"),
            )

# async def get_token(username: str, password: str) -> Token:
#     # token_url = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"
#     token_url = "http://localhost:8080/realms/EST/protocol/openid-connect/token"
#     data = {
#         "client_id": "fastapi-keycloak",
#         "client_secret": "UtKSPKwHM0doSACshE9iD99xyJO6l15r",
#         "grant_type": "password",
#         "username": username,
#         "password": password,
#     }
#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.post(token_url, data=data)
#             print("Keycloak Response:", response.status_code, response.text)

#             if response.status_code != 200:
#                 raise Exception(f"Keycloak error: {response.json()}")

#             token_data = response.json()
#             return Token(access_token=token_data["access_token"], token_type=token_data["token_type"])
#     except Exception as e:
#         raise Exception(f"Token request failed: {str(e)}")
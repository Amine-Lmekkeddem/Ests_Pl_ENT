from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str = None
    refresh_expires_in: int = None

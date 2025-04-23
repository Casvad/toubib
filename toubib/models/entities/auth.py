from pydantic.main import BaseModel

class AuthSession(BaseModel):
    email: str

class AuthOut(AuthSession):
    token: str
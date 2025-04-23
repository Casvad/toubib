from pydantic.main import BaseModel
from pydantic.networks import EmailStr

class UserIn(BaseModel):
    email: EmailStr
    password: str


class UserModel(BaseModel):
    email: EmailStr
    id: int

    class Config:
        orm_mode = True
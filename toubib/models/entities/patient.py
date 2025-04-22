from datetime import date
from enum import Enum

from pydantic.main import BaseModel
from pydantic.networks import EmailStr


class SexAtBirth(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

class PatientIn(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    date_of_birth: date
    sex_at_birth: SexAtBirth


class PatientModel(PatientIn):
    id: int

    class Config:
        orm_mode = True
from datetime import date

from pydantic.main import BaseModel


class DoctorIn(BaseModel):
    first_name: str
    last_name: str
    hiring_date: date
    specialization: str

class DoctorModel(DoctorIn):
    id: int

    class Config:
        orm_mode = True
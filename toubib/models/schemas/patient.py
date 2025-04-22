from sqlalchemy import Column, Date, Integer, String
from fastapi_sqla import Base

class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    date_of_birth = Column(Date, nullable=False)
    sex_at_birth = Column(String, nullable=False)
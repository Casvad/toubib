from sqlalchemy import Column, Date, Integer, String
from fastapi_sqla import Base

class Doctor(Base):
    __tablename__ = "doctor"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hiring_date = Column(Date, nullable=False)
    specialization = Column(String, nullable=False)
from sqlalchemy import Column, Integer, String, Float
from .database import Base

class ExtractedClaim(Base):
    __tablename__ = "extracted_claims"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=False)
    sex = Column(String(10), nullable=False)
    bmi = Column(Float, nullable=False)
    children = Column(Integer, nullable=False)
    region = Column(String(50), nullable=False)
    charges = Column(Float, nullable=False)

def __repr__(self):
    return f"<ExtractedClaim(id={self.id}, age={self.age}, sex='{self.sex}', bmi={self.bmi}, charges={self.charges})>"
from sqlalchemy import Column, Integer, String, Float
from database.db import Base

class OperationHistory(Base):
    __tablename__ = "operation_history"
    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String, index=True)
    operand1 = Column(Float, nullable=False)
    operand2 = Column(Float, nullable=False)
    result = Column(Float, nullable=False)

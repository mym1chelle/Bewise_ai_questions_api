from sqlalchemy import Column, Integer, DateTime, Text, BigInteger
import datetime
from data.db import Base


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(BigInteger, nullable=False, unique=True)
    question_text = Column(Text, nullable=False)
    answer_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True))
    added = Column(DateTime, default=datetime.datetime.utcnow)

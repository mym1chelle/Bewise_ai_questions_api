from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ExtendedModel(BaseModel):
    class Config:
        orm_mode = True


class AddQuestionModel(ExtendedModel):
    questions_num: int = Field(ge=1, le=100, default=1)


class QuestionReturnsModel(ExtendedModel):
    id: Optional[int]
    question_id: Optional[int]
    question_text: Optional[str]
    answer_text: Optional[str]
    created_at: Optional[datetime]
    added: Optional[datetime]

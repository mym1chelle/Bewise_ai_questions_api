from pydantic import BaseModel, Field


class ExtendedModel(BaseModel):
    class Config:
        orm_mode = True


class AddQuestionModel(ExtendedModel):
    questions_num: int = Field(ge=1)
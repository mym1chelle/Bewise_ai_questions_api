from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from data.db import get_async_session
from typing import List
from questions_api.schemas import AddQuestionModel, QuestionReturnsModel
from questions_api.models import Question
from questions_api.engine import (
    save_missing_questions,
    get_last_saved_question
)

router = APIRouter(
    tags=['Questions']
)


@router.get('/questions', response_model=List[QuestionReturnsModel])
async def get_questions(
        limit: int = 15,
        offset: int = 0,
        session: AsyncSession = Depends(get_async_session)
):
    """Выводит список всех вопросов"""
    query = select(Question).limit(limit).offset(offset)
    result = await session.execute(query)
    return result.scalars().all()


@router.post('/questions', response_model=QuestionReturnsModel)
async def add_question(
        count: AddQuestionModel,
        session: AsyncSession = Depends(get_async_session)
):
    """Добавление вопросов"""
    last = await get_last_saved_question(session=session)
    data = count.dict()
    question_count = data['questions_num']
    await save_missing_questions(
        question_count=question_count,
        session=session
    )
    return last

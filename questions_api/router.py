from fastapi import APIRouter, Depends, HTTPException
from dateutil.parser import parse
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from data.db import get_async_session
from questions_api.schemas import AddQuestionModel
from questions_api.models import Question
from questions_api.engine import save_missing_questions
# from questions_api.schemas

load_dotenv()

router = APIRouter(
    prefix='/cards',
    tags=['Cards']
)


@router.get('/questions')
async def get_questions(
        limit: int = 15,
        offset: int = 0,
        session: AsyncSession = Depends(get_async_session)
):
    """Выводит список всех вопросов"""
    query = select(Question).limit(limit).offset(offset)
    result = await session.execute(query)
    return result.scalars().all()


@router.post('/questions')
async def add_question(
        count: AddQuestionModel,
        session: AsyncSession = Depends(get_async_session)
):
    """Добавление карточки"""

    data = count.dict()
    question_count = data['questions_num']
    await save_missing_questions(
        question_count=question_count,
        session=session
    )
    return 2
import aiohttp
from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from questions.models import Question
from dateutil.parser import parse
from data.config import load_config


config = load_config(".env")


async def get_response(count: int = 1):
    sevice = config.service.base_url
    url = f'{sevice}count={count}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail='API service with questions not answered'
                )


async def is_question_exist(question_id: int, session: AsyncSession):
    query = select(Question).where(Question.question_id == question_id)
    result = await session.execute(query)
    question = result.scalars().first()
    if question:
        return True
    return False


async def get_unique_questions(
        session: AsyncSession,
        question_count: int = 1
):
    unique_questions = []
    while len(unique_questions) < question_count:
        questions_response = await get_response(
            count=question_count - len(unique_questions)
        )
        for question in questions_response:
            question_id = question.get('id')
            exist = await is_question_exist(
                question_id=question_id,
                session=session
            )
            if not exist:
                question_data = {
                    'question_id': question.get('id'),
                    'question_text': question.get('question'),
                    'answer_text': question.get('answer'),
                    'created_at': parse(question.get('created_at'))
                }
                unique_questions.append(question_data)
    return unique_questions


async def save_missing_questions(question_count, session: AsyncSession):
    questions = await get_unique_questions(
        question_count=question_count,
        session=session
    )
    for question in questions:
        new_question = Question(**question)
        session.add(new_question)
    await session.commit()


async def get_last_saved_question(session: AsyncSession):
    query = select(Question).order_by(Question.added.desc())
    return (await session.execute(query)).scalars().first()

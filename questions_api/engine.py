import aiohttp
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from questions_api.models import Question
from dateutil.parser import parse


async def get_response(count: int = 1):
    sevice = os.getenv('QUESTION_URL')
    url = f'{sevice}count={count}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(f'get response {count}')
            return await response.json()


class QuestionManager:
    def __init__(self, session):
        self.session = session


async def get_question(question_id: int, session: AsyncSession):
    query = select(Question).where(Question.question_id == question_id)
    result = await session.execute(query)
    question = result.scalars().first()
    if question:
        return True
    return False


async def search_question(
        session: AsyncSession,
        question_count: int = 1
):
    unique_questions = []
    while len(unique_questions) < question_count:
        questions_response = await get_response(count=question_count - len(unique_questions))
        for question in questions_response:
            question_id = question.get('id')
            question_is_exist = await get_question(
                question_id=question_id,
                session=session
            )
            if not question_is_exist:
                question_data = {
                    'question_id': question.get('id'),
                    'question_text': question.get('question'),
                    'answer_text': question.get('answer'),
                    'created_at': parse(question.get('created_at'))
                }
                unique_questions.append(question_data)
    return unique_questions


async def add_new_question(question_count, session: AsyncSession):
    questions = await search_question(
        question_count=question_count,
        session=session
    )
    print('END', len(questions))
    for question in questions:
        new_question = Question(**question)
        session.add(new_question)
    await session.commit()
    return 1
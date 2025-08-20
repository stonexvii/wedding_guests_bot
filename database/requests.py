from aiogram.types import Message

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import config
from .db_engine import async_session, engine
from .tables import Base, AnswersTable, QuestionsTable, Users, UserAnswers


def connection(function):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            try:
                return await function(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper


async def create_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)


@connection
async def add_user(user_tg_id: int, user_name: str, session: AsyncSession):
    user_db = await session.scalar(select(Users).where(Users.id == user_tg_id))
    if not user_db:
        session.add(Users(id=user_tg_id, username=user_name))
        await session.commit()


@connection
async def set_question(question_id: int, question_text: str, answers: list[str], session: AsyncSession):
    question = await session.scalar(select(QuestionsTable).where(QuestionsTable.id == question_id))
    if question:
        await delete_question(question_id)
    question = QuestionsTable(id=question_id, question=question_text)
    session.add(question)
    await session.commit()
    answers = [AnswersTable(question_id=question_id, answer_id=answer_id, answer=answer) for answer_id, answer in
               enumerate(answers, 1)]
    session.add_all(answers)
    await session.commit()


@connection
async def delete_question(question_id: int, session: AsyncSession):
    question = await session.scalar(select(QuestionsTable).where(QuestionsTable.id == question_id))
    if question:
        await session.delete(question)
        await session.commit()


@connection
async def get_question(question_id: int, session: AsyncSession):
    question = await session.scalar(select(QuestionsTable).where(QuestionsTable.id == question_id))
    if question:
        answers = await session.scalars(
            select(AnswersTable).where(AnswersTable.question_id == question_id))
        return question, answers.all()


@connection
async def add_user_answer(user_id: int, question_id: int, answer_id: int, session: AsyncSession):
    session.add(UserAnswers(
        user_id=user_id,
        question_id=question_id,
        answer_id=answer_id,
    ))
    await session.commit()


@connection
async def collect_answers(question_id: int, session: AsyncSession):
    response = await session.scalars(select(UserAnswers.answer_id).where(UserAnswers.question_id == question_id))
    return response.all()


@connection
async def all_users(session: AsyncSession):
    response = await session.scalars(select(Users.id))
    return response.all()


@connection
async def all_questions(session: AsyncSession):
    response = await session.scalars(select(QuestionsTable))
    return response.all()


@connection
async def delete_answers(question_id: int, session: AsyncSession):
    answers = await session.scalars(select(UserAnswers).where(UserAnswers.question_id == question_id))
    for answer in answers.all():
        await session.delete(answer)
    await session.commit()

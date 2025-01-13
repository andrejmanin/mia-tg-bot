from database.models import async_session
from database.models import User
from sqlalchemy import select, update
import json


async def set_user(tg_id, name: str, history=None):
    if history is None:
        history = [{"role": "developer", "content": "You are czech friend Mia."}]
    async with async_session() as session:
        user = await get_user(tg_id)
        if user is None:
            session.add(User(tg_id=tg_id, name=name, history=json.dumps(history)))
            await session.commit()


async def get_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            return None
        return user

async def update_user_history(tg_id, history):
    async with async_session() as session:
        async with session.begin():
            user = await get_user(tg_id)
            if len(user.history) > 9000:
                del user.history[1:(len(user.history) // 2)]
                await session.commit()
            stmt = (update(User).where(User.tg_id == tg_id).values(history=json.dumps(history)))
            await session.execute(stmt)
            await session.commit()
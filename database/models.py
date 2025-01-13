from sqlalchemy import BigInteger, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///mia.db')
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    tg_id = mapped_column(BigInteger, nullable=False)
    name: Mapped[str] = mapped_column(String(35), nullable=False)
    history = mapped_column(Text(10000))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
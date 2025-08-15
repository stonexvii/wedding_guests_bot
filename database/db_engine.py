from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import config

engine = create_async_engine(
    url=config.DB_URL,
    echo=False,
)

async_session = async_sessionmaker(engine)

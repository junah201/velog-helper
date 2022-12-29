from fastapi_utils.session import FastAPISessionMaker

from app.database import models
from app.database.database import engine
from app.common.config import SQLALCHEMY_DATABASE_URL
from app.tasks import new_post

import asyncio

models.Base.metadata.create_all(bind=engine)

sessionmaker = FastAPISessionMaker(SQLALCHEMY_DATABASE_URL)


def lambda_handler(event, context):
    with sessionmaker.context_session() as db:
        asyncio.run(new_post.update_new_post(db))

from sqlmodel import create_engine, SQLModel, Session
from configs.settings import ENVS, BASE_DIR

from songs import models


DATABASE_URL = f"postgresql://{ENVS.POSTGRES_USER}:{ENVS.POSTGRES_PASSWORD}@{ENVS.POSTGRES_HOST}:{ENVS.POSTGRES_PORT}/{ENVS.POSTGRES_DB}"
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

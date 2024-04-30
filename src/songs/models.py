
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel
from .app import app_name


class SongBase(SQLModel):
    name: str
    artist: str
    created_at: datetime = Field(
        nullable=True, 
        default_factory=lambda: datetime.now()
    )
    updated_at: datetime = Field(
        nullable=True,
        default_factory=lambda: datetime.now(timezone.utc),
    )


class Song(SongBase, table=True):
    __tablename__ = f"{app_name}_songs"
    id: int | None = Field(default=None, primary_key=True)


class SongCreate(SongBase):
    pass

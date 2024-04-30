from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlmodel import Session, select

from configs.db import init_db, get_session
from songs.models import Song, SongCreate


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("starup event")
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/ping")
def pong():
    return {"ping": "pong!"}

@app.post("/songs")
def add_song(song: SongCreate, session: Session = Depends(get_session)):
    song = Song(name=song.name, artist=song.artist)
    session.add(song)
    session.commit()
    session.refresh(song)
    return song


@app.get("/songs", response_model=list[Song])
async def get_songs(session: Session = Depends(get_session)):
    result = session.execute(select(Song))
    songs = result.scalars().all()
    return [Song(name=song.name, artist=song.artist, id=song.id) for song in songs]

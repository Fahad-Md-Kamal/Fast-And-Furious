from pstats import Stats
from fastapi import (
    Depends,
    status,
    HTTPException,
    APIRouter
)
from sqlalchemy.orm import Session

from app import oauth2

from .. import models, schemas, utils
from ..database import get_db


router = APIRouter(
    prefix="/votes",
    tags=['VOTE']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def votet(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {vote.post_id} does not existis')

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, 
        models.Vote.user_id == current_user.id
        )
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'user {current_user.id} has already voted on post {vote.post_id}')
        new_vote = models.Vote(post_id = vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete()
        db.commit()
        
        return {"message":"successfully deleted vote"}

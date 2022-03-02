from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

from app import models
from . import schemas, database
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token

def verify_access_token(token: str, credentials_expception):
    """Verify JWT access token and return user id"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if not id:
            raise credentials_expception
        
        token_data = schemas.TokenData(id=id)
        return token_data
    except JWTError:
        raise credentials_expception


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)) -> schemas.UserResponse:
    """Setup HTTP exception Error for the token Validation and return current uer data"""
    credentials_expception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Could not validate credentials",
        headers={"www-Authenticate": "Bearer"}
    )
    token = verify_access_token(token, credentials_expception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user

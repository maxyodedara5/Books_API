from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import os
from os.path import dirname, join
from dotenv import load_dotenv
import schemas, database, models
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception: Exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        
        # If issue, change the algorithms=ALGORITHM to algorithms=[ALGORITHM]
        id : str = payload.get("user_id")
        if id is None: 
            raise credentials_exception 
        

        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)) -> (models.User): 
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception) 

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
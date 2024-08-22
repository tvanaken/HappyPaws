import os
from typing import Annotated

from app.models.user import User
from app.utils import get_session
from dotenv import load_dotenv
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



class Token(BaseModel):
    """
    Represents a token used for authentication.

    Attributes:
        access_token (str): The access token.
        token_type (str): The type of the token.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Represents the data contained in a token.

    Attributes:
        email (str, optional): The email associated with the token. Defaults to None.
    """
    email: str | None = None


class AccessToken(BaseModel):
    """
    Represents an access token.

    Attributes:
        access_token (str): The access token string.
        token_type (str): The type of the token.
    """
    access_token: str
    token_type: str



async def get_current_user(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)
) -> User:
    """
    Retrieves the current user based on the provided token.
    Parameters:
        token (str): The authentication token.
        session (AsyncSession): The database session.
    Returns:
        User: The current user.
    Raises:
        HTTPException: If the credentials cannot be validated.
    """
    from app.routers.users import get_user_by_email

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        # payload not encrypted, try using user_id
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_email(email=token_data.email, session=session)
    if user is None:
        raise credentials_exception
    return user

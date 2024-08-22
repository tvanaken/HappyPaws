from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


app = Flask(__name__)
bcrypt = Bcrypt(app)


class UserCreate(BaseModel):
    """
    UserCreate model represents the data required to create a new user.

    Attributes:
    - email (str): The email address of the user.
    - password (str): The password of the user.

    """
    email: str
    password: str


class Token(BaseModel):
    """
    Token model class.

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


class User(Base):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier of the user.
        email (str): The email address of the user.
        password (str): The password of the user.
        pets (List[Pet]): The list of pets associated with the user.
        comments (List[Comment]): The list of comments made by the user.

    Methods:
        set_password(password: str) -> None:
            Sets the password for the user.
        
        check_password(password: str) -> bool:
            Checks if the provided password matches the user's password.

    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(254), unique=True, index=True)
    password = Column(String(254))

    pets = relationship("Pet", back_populates="user", cascade="all, delete")
    comments = relationship("Comment", back_populates="user")

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

from sqlalchemy import Column, Integer, String
from .base import Base
from sqlalchemy.orm import relationship
from flask import Flask, request, jsonify
from pydantic import BaseModel
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)


class UserCreate(BaseModel):
    email: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class AccessToken(BaseModel):
    access_token: str
    token_type: str

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True) 
    email = Column(String(254), unique=True, index=True)
    password = Column(String(254))

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

pets = relationship("Pet", back_populates="user", cascade="all, delete")
from typing import Annotated, Literal
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field, EmailStr
from fastapi import Depends, FastAPI



class User(BaseModel):
    user_id : int
    email: EmailStr
    password : str = Field(min_length=8)

class U(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class UN(BaseModel):
    email: EmailStr

class UNP(BaseModel):
    password: str = Field(min_length=8)


class UR(BaseModel):
    role: str

class Hash(BaseModel):
    password: str = Field(min_length=8)

class PostPost(BaseModel):
    content: str

class PU(BaseModel):
    author_email: EmailStr




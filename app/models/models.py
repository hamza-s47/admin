from pydantic import BaseModel
from datetime import datetime

class Admin(BaseModel):
    email:str
    password:str

class FormData(BaseModel):
    name:str
    email:str
    contact:str | None = None
    message:str
    time: datetime

class Projects(BaseModel):
    title:str
    description:str
    url:str
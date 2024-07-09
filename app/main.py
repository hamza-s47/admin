from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pymongo import MongoClient
from pydantic import BaseModel

class Item(BaseModel):
    uid:str
    movie:str
    rating:float


app = FastAPI()
conn = MongoClient("mongodb+srv://hamza:1234@mycluster.438n2qs.mongodb.net/?retryWrites=true&w=majority&appName=myCluster")

@app.get("/", response_class=HTMLResponse)
def home():
    return "<h1>Python - FastAPI<h1>"


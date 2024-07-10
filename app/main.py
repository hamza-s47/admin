from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from pymongo import MongoClient
from pydantic import BaseModel

class Item(BaseModel):
    uid:str
    movie:str
    rating:float


app = FastAPI()
conn = MongoClient("mongodb+srv://hamza:1234@mycluster.438n2qs.mongodb.net/?retryWrites=true&w=majority&appName=myCluster")
app.mount("/static", StaticFiles(directory="./app/static"), name="static")  #For CSS (static) file
templates = Jinja2Templates(directory="./app/view")  #For HTML file

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "name": "Home"})

@app.get("/about", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "name": "About"})


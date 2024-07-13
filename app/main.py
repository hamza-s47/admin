from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime
from pymongo import MongoClient
from pydantic import BaseModel
import secrets

class Admin(BaseModel):
    email:str
    password:str
class FormData(BaseModel):
    name:str
    email:str
    contact:str | None = None
    message:str
    time: datetime

app = FastAPI()
origins = [
    "http://localhost:8000",       
    "https://hamzasiddiqui.netlify.app"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows methods like (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)
app.add_middleware(SessionMiddleware, secret_key=secrets.token_hex(32))
client = MongoClient("mongodb+srv://hamza:1234@mycluster.438n2qs.mongodb.net/?retryWrites=true&w=majority&appName=myCluster")
db = client.portfolio.contact
admin_db = client.portfolio.admin
app.mount("/static", StaticFiles(directory="./app/static"), name="static")  #For CSS (static) file
templates = Jinja2Templates(directory="./app/view")  #For HTML file

@app.get("/login", response_class=HTMLResponse)
def home(request: Request):
    if request.session.get("isLoggedin"):
        RedirectResponse(url='/')
        
    return templates.TemplateResponse("index.html", {"request": request, "name": "M HAMZA SIDDIQUI"})

@app.post("/login")
async def update_login(req:Request, data:Admin):
    check = admin_db.find_one()
    if (data.email == check['email'] or data.email == check['user_name']) and data.password == check['password']:
        req.session["isLoggedin"] = True
        print("login POST route: ", req.session.get("isLoggedin"))
        return RedirectResponse(url= '/')
    return RedirectResponse(url='/login')
    
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    data = db.find()
    if request.session.get("isLoggedin"):
        print("it is comming to get root route")
        return templates.TemplateResponse("contact.html", {"request": request, "form": data})
    
    print("it is comming to get root route but not redirecting: ", request.session.get("isLoggedin"))
    return RedirectResponse(url='/login')

@app.post("/contact")
async def submit_form(form:FormData):
    form_dict = form.model_dump()
    # form_dict["time"] = datetime.now()
    db.insert_one(form_dict)
    #print(form)
    return { "message": "Success!" }


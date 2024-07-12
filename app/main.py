from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pymongo import MongoClient
from pydantic import BaseModel

class Admin(BaseModel):
    email:str
    password:str
    isLoggedin:bool = False
class FormData(BaseModel):
    name:str
    email:str
    contact:str | None = None
    message:str
    time: datetime

app = FastAPI()
origins = [
    "http://localhost:4200",       
    "https://hamzasiddiqui.netlify.app"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows methods like (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)
client = MongoClient("mongodb+srv://hamza:1234@mycluster.438n2qs.mongodb.net/?retryWrites=true&w=majority&appName=myCluster")
db = client.portfolio.contact
admin_db = client.portfolio.admin
app.mount("/static", StaticFiles(directory="./app/static"), name="static")  #For CSS (static) file
templates = Jinja2Templates(directory="./app/view")  #For HTML file

@app.get("/login", response_class=HTMLResponse)
def home(request: Request):
    check = admin_db.find_one()['isLoggedin']
    if check:
        RedirectResponse(url='/')
        
    return templates.TemplateResponse("index.html", {"request": request, "name": "M HAMZA SIDDIQUI"})

@app.put("/login")
async def update_login(data:Admin):
    check = admin_db.find_one()
    if data.email == check['email'] and data.password == check['password']:
        admin_db.update_one({"email": data.email}, {"$set": {"isLoggedin": True}})
        return RedirectResponse(url= '/')
    return RedirectResponse(url='/login')
    
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    data = db.find()
    check = admin_db.find_one()['isLoggedin']
    if check:
        return templates.TemplateResponse("contact.html", {"request": request, "form": data})
    
    return RedirectResponse(url='/login')

@app.post("/contact")
async def submit_form(form:FormData):
    form_dict = form.model_dump()
    form_dict["time"] = datetime.now()
    db.insert_one(form_dict)
    #print(form)
    return { "message": "Success!" }


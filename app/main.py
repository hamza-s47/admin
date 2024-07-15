from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from pymongo import MongoClient
import gridfs
from pathlib import Path
import secrets
import app.models.models as schema


app = FastAPI()

origins = [
    "http://localhost:8000",
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
app.add_middleware(SessionMiddleware, secret_key=secrets.token_hex(32))

client = MongoClient("mongodb+srv://hamza:1234@mycluster.438n2qs.mongodb.net/?retryWrites=true&w=majority&appName=myCluster")
db = client.portfolio.contact
admin_db = client.portfolio.admin
fs = gridfs.GridFS(client.portfolio)

app.mount("/static", StaticFiles(directory="./app/static"), name="static")  #For CSS (static) file
templates = Jinja2Templates(directory="./app/view")  #For HTML file

#Root Route
@app.get('/', response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse('home.html', {"request": request, "show_header": True})
    # if request.session.get("isLoggedin"):
    #     return templates.TemplateResponse('home.html', {"request": request, "show_header": True})
    # return RedirectResponse(url="/login")

#Upload Routes
@app.post('/resume')
async def upload_resume(file: UploadFile = File(...)):
    try:
        fs.put(file.file, filename=file.filename)
        return {"info": f"file {file.filename} saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {e}")

#Auth Root
@app.get("/login", response_class=HTMLResponse)
def get_login(request: Request):
    if request.session.get("isLoggedin"):
        RedirectResponse(url='/messages')
        
    return templates.TemplateResponse("login.html", {"request": request, "show_header": False})

@app.post("/login")
async def login(req:Request, data:schema.Admin):
    check = admin_db.find_one()
    if (data.email == check['email'] or data.email == check['user_name']) and data.password == check['password']:
        req.session["isLoggedin"] = True
        print("login POST route: ", req.session.get("isLoggedin"))
        return RedirectResponse(url= '/messages')
    return RedirectResponse(url='/login')

@app.post("/logout")
async def logout(request: Request):
    request.session["isLoggedin"] = False
    return RedirectResponse(url="/login", status_code=303)

#Projects Route
@app.get("/projects")
async def get_project(request:Request):
    return templates.TemplateResponse('projects.html', {"request": request, "show_header": True})

    # if request.session.get("isLoggedin"):
    #     return templates.TemplateResponse('projects.html', {"request": request, "show_header": True})
    # return RedirectResponse(url="/login")

# Messages Route
@app.get("/messages", response_class=HTMLResponse)
def get_contacts(request: Request):
    data = db.find()
    if request.session.get("isLoggedin"):
        print("it is comming to get root route")
        return templates.TemplateResponse("contact.html", {"request": request, "form": data, "show_header": True})
    
    print("it is comming to get root route but not redirecting: ", request.session.get("isLoggedin"))
    return RedirectResponse(url='/login')

@app.post("/contact")
async def contacts(form:schema.FormData):
    form_dict = form.model_dump()
    # form_dict["time"] = datetime.now()
    db.insert_one(form_dict)
    #print(form)
    return { "message": "Success!" }


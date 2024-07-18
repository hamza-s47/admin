from fastapi import FastAPI, File, UploadFile, HTTPException, Response, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from pymongo import MongoClient
import bson.binary
from bson import ObjectId
import secrets
import app.models.models as schema


app = FastAPI()

origins = [
    # "http://localhost:8000",
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
db = client.portfolio

app.mount("/static", StaticFiles(directory="./app/static"), name="static")  #For CSS (static) file
templates = Jinja2Templates(directory="./app/view")  #For HTML file

#Root Route
@app.get('/', response_class=HTMLResponse)
async def home(request:Request):
    if request.session.get("isLoggedin"):
        return templates.TemplateResponse('home.html', {"request": request, "show_header": True})
    return RedirectResponse(url="/login")

#Image Routes
@app.get("/image")
async def show_image():
    try:
        file_document = db.uploads.find_one({})
        if not file_document:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Return the file as a response with content type image/jpeg
        return Response(content=file_document["data"], media_type=file_document["content_type"])
        
    except Exception as e:
        # return {"message": "Internal Server   Error", "status":500}
        raise HTTPException(status_code=500, detail=f"Failed to retrieve file: {e}")

@app.put('/image')
async def image(file: UploadFile = File(...)):
    MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB
    file_size = await file.read()
    if len(file_size) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds the 2MB limit.")
    try:
        file_data = bson.binary.Binary(file_size)
        db.uploads.update_one({"_id": bson.ObjectId("669626a473d94fc92ea03758")},{"$set": {
            "filename": file.filename,
            "content_type": file.content_type,
            "data": file_data
            }
        })
        return {"file": file.filename, "message":"Upload successfully!" }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {e}")

#Auth Root
@app.get("/login",  response_class=HTMLResponse)
def get_login(request: Request):
    if request.session.get("isLoggedin"):
        RedirectResponse(url='/')
        
    return templates.TemplateResponse("login.html", {"request": request, "show_header": False})

@app.post("/login")
async def login(request:Request, data:schema.Admin):
    check = db.admin.find_one()
    if (data.email == check['email'] or data.email == check['user_name']) and data.password == check['password']:
        request.session["isLoggedin"] = True
        print("login POST route: ", request.session.get("isLoggedin"))
        return RedirectResponse(url= '/')
    return RedirectResponse(url='/login')

@app.get("/logout")
async def logout(request: Request):
    request.session["isLoggedin"] = False
    return RedirectResponse(url="/login", status_code=303)

#Projects Route
@app.get("/projects")
async def get_project(request:Request):
    data = db.projects.find()
    projects = [{**project, "_id": str(project["_id"])} for project in data]   
    if request.session.get("isLoggedin"):
        return templates.TemplateResponse("projects.html", {"request": request, "projects": projects, "show_header": True})
    
    return RedirectResponse(url='/login')

@app.post('/projects')
async def projects(title: str = Form(...), description: str = Form(...), url: str = Form(...)):
    data_dict = schema.Projects(title=title, description=description, url=url).model_dump()
    db.projects.insert_one(data_dict)
    return {"message": "Successfully added!", "status":200}

@app.put("/update-project/{project_id}")
async def update_project(project_id: str, title: str = Form(...), description: str = Form(...), url: str = Form(...)):
    project = {
        "title": title,
        "description": description,
        "url": url
    }
    result = db.projects.update_one({"_id": ObjectId(project_id)}, {"$set": project})
    if result.modified_count == 1:
        return {"message": "Project updated successfully", "status": 200}
    
    return {"message": "Project not found or not updated", "status": 404}

# Messages Route
@app.get("/messages", response_class=HTMLResponse)
def get_contacts(request: Request):
    data = db.messages.find()
    if request.session.get("isLoggedin"):
        print("it is comming to get root route")
        return templates.TemplateResponse("contact.html", {"request": request, "messages": data, "show_header": True})
    
    print("it is comming to get root route but not redirecting: ", request.session.get("isLoggedin"))
    return RedirectResponse(url='/login')

@app.post("/messages")
async def contacts(form:schema.FormData):
    form_dict = form.model_dump()
    # form_dict["time"] = datetime.now()
    db.messages.insert_one(form_dict)
    #print(form)
    return { "message": "Success!" }


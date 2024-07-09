python3.12 -m uvicorn main:app --host 0.0.0.0 --reload
python3.12 -m uvicorn app.main:app --host 0.0.0.0 --reload

-> Virtual ENV:
pip install virtualenv
python -m venv myenv
source myenv/bin/activate (Linux / MacOS)
myenv\Scripts\activate.bat (Windows)
myenv\Scripts\activate.ps1 (Windows from powershell)

deactivate (To exit from venv)

-> Place your versions in a .txt file for other devs:
pip freeze (Show the versions of all of your packages)
pip freeze > requirements.txt (Write those versions in a seperate .txt file)
pip install -r requirements.txt (Install all the versions from that .txt file)





@app.get("/mov")
async def show_movies():
    response = conn.netflix.movies.find_one({})
    
    if response:
        #response["id"] = str(response["_id"])  # Convert ObjectId to str
        del response["_id"]  # Remove the ObjectId from the document
        
    print(response)
    return response

@app.post("/movies")
async def update_item(item: Item,):
    if item.rating > 5 or item.rating < 0:
        print("Rating should be between 0-5")
        return "WTF man!"
    else:
        conn.netflix.movies.insert_one(item.model_dump())
        print(item.model_dump())
        return

@app.delete("/remove/{uid}")
async def delete_movie(uid:str):
    doc = conn.netflix.movies.delete_one({"uid": uid})
    print(doc)
    return

@app.put("/update/{uid}")
async def update_movie(uid:str, item:Item):
    doc = conn.netflix.movies.update_one({"uid":uid}, {"$set": item.model_dump()})
    print(doc)
    return



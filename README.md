python3.12 -m uvicorn main:app --host 0.0.0.0 --reload
python3.12 -m uvicorn app.main:app --host 0.0.0.0 --reload
----------------------------------------------------------------------------------

-> Virtual ENV:
pip install virtualenv
python -m venv myenv
source myenv/bin/activate (Linux / MacOS)
myenv\Scripts\activate.bat (Windows)
myenv\Scripts\activate.ps1 (Windows from powershell)

deactivate (To exit from venv)
----------------------------------------------------------------------------------

-> Place your versions in a .txt file for other devs:
pip freeze (Show the versions of all of your packages)
pip freeze > requirements.txt (Write those versions in a seperate .txt file)
pip install -r requirements.txt (Install all the versions from that .txt file)
----------------------------------------------------------------------------------

DEPLOY ON VERCEL:
sudo npm i -g vercel
vercel login (Github)
vercel .
directory... (./)  --> Press enter only for root directory
link to .... (n)
... etc
----------------------------------------------------------------------------------

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  (github token)

/lib/python3.12/EXTERNALLY-MANAGED
OR
/usr/lib/python3.12/EXTERNALLY-MANAGED  (Remove with sudo)
----------------------------------------------------------------------------------

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
----------------------------------------------------------------------------------

MONGO-DB CHEAT SHEAT:

-> Use Particular Database:
use database_name


-> Adding Docs:
db.collection_name.insertOne({})
db.collection_name.insertMany([{}, {}, {}])


-> Finding Docs:
db.collection_name.find()   // it will give us first 20 documents.
it                            // Now it will give 20 more documents (iterate).
db.collection_name.find({key:"value"})     // it will find/give the filtered data now.
db.books.find({type:"Planet"}, {name:1, _id:0})     // it will give only name fields which have type Planet.
db.books.find({rating:{$gt:5}})              // it will give all docs which have rating greater than 5.
db.books.find({rating:{$lt:5}})              // it will give all docs which have rating less than 5.
db.books.find({rating:{$lte:5}})             // it will give all docs which have rating less than or equals to 5.
db.books.find({$or: [{rating:{$gte:5}, {name:"Mercury"}, {type:"Planet"}}]})     // it has many filters.
db.books.find({rating: {$in: [4,8,9]}})      // it will give those which have these (4,8,9) ratings.
db.books.find({rating: {$nin: [4,8,9]}})      // it will give those which don't have these (4,8,9) ratings.
db.books.find({genres: {$all: ["sci-fi", "fantasy"]}})   // it will give those docs have minimum these values presented.
db.books.find({"projects.name": "Project A"})
db.books.findAndModify({
   query:{_id: ObjectId("64faaeb4d058a2b481b8634e")},
   update: {$inc: {salary: 1000}},
   new: true
})       // it will update and show the salary immediately (reduce update and find method).


-> Counting & Limiting the Docs:
db.books.find().count()                                 // it will count documents for us.
db.collection_name.find({key:"value"}).count()        // it will count the filtered docs.
db.books.find().limit(3)                                // it will only show 3 docs.
db.books.find().count({salary: {$gt: 10000}})           // it will show the counts of 10k+ salary docs.


-> Sorting Docs:
db.books.find.sort({name: 1})                  // it will sort by name in ASC order.
db.books.find.sort({name: -1})                 // it will sort by name in DESC order.
db.books.find.sort({type: -1}).limit(4)        // it will sort by type in DESC order and give 4 docs.
db.books.find({salary: {$lte: 40000}}).sort({name: 1})


-> Deleting Docs:
db.db.books.deleteOne({_id: ObjectId("...")})    // it will delete only one doc by ID.
db.db.books.deleteMany({type:"Planet"})          // it will delete all docs which have type Planet.
db.books.remove({})                              // it will delete all docs from the collection.


-> Updating Docs:
db.books.updateOne({_id: ObjectId("64faaeb4d058a2b481b8634c")}, {$set: {firstName: "Doe", lastName:"Jonn"}})
db.books.updateMany({department: "Finance"}, {$set: {department: "IT"}})
db.books.updateOne({_id: ObjectId("64faaeb4d058a2b481b8634e")}, {$inc: {salary: 5000}})
db.books.updateOne({_id: ObjectId("64faaeb4d058a2b481b8634e")}, {$pull: {genre: "Fantasy"}})
db.books.updateOne({_id: ObjectId("64faaeb4d058a2b481b8634e")}, {$push: {genre: "Horror"}})
db.books.updateOne({_id: ObjectId("64faaeb4d058a2b481b8634e")}, {$push: {genre: {$each: ["Tech", "Dark"]}}})
db.books.updateMany(
  { publishedDate: { $lt: new Date("2019-01-01") } },
  { $set: { status: "LEGACY" } }
)


-> Replacing Docs:
db.books.replaceOne({_id: ObjectId("64faaeb4d058a2b481b8634e")}, {name:"Pluto", size:"small"})    //Replace the name and size field with the given value.

-> Get From Reference:
db.customer.aggregate({ $lookup: { from: ”address(collection)”, localField: “address(key)”, foreignField: “_id”, as: “addr” } })

customer is a collection
from address collection
localField is address key of customer collection
foreignField is the key of address collection and storing as reference in customer collection
as addr name key will be shown in customer collection when fetched from $lookup.

We use Embedded Relation where no redundancy:
One to One , One to Many, Many to One

We use References where redundancy occurs:
Many to Many

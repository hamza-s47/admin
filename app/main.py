from fastapi import FastAPI
from pymongo import MongoClient


app = FastAPI()
conn = MongoClient("mongodb+srv://hamza:1234@mycluster.438n2qs.mongodb.net/?retryWrites=true&w=majority&appName=myCluster")

@app.get("/")
def home():
    docs=conn.netflix.watchlist.insert_many([
        {"movie":"POTSV", "watched":True,},
        {"movie":"Enigma", "watched":False,},
        {"movie":"No escape", "watched":False}
        ])
    print(docs)
    return "Hello World!"
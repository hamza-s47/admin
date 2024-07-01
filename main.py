from fastapi import FastAPI
import rps

app = FastAPI()

@app.get("/")
def home():
    return {"HW":"Hello World!"}

@app.get("/rps")
def abc():
    Result = ""
    
    if rps.scorePerson > rps.scoreComp:
        Result = "Person won!"
    elif rps.scoreComp > rps.scorePerson:
        Result = "Computer won!"
    else: Result = "Tied!"
    
    return {"Computer Score" : rps.scoreComp, "Person Score" : rps.scorePerson, "Result" : Result}
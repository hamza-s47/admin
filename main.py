from fastapi import FastAPI
import rps

app = FastAPI()

@app.get("/")
def home():
    return {"HW":"Hello World!"}

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from main import getData_from_fastAPI

# CORS import
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class userQuery(BaseModel):
    message: str

class sendDatafromjarvis(BaseModel):
    reply: str    

@app.post('/send')
def send_to_model(input: userQuery):
    user_message = input.message
    print("Received from Flutter:", user_message)
    response = getData_from_fastAPI(user_message)
    if response != None:
        print("Response sent:", response)

    return {
        "reply": response
    }

@app.get('/')
def root():
    return print("Server line on: 8000")
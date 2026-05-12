from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import subprocess
import os

app = FastAPI()

# create output folder if not exists
os.makedirs("output", exist_ok=True)

# serve output folder
app.mount("/output", StaticFiles(directory="output"), name="output")

@app.get("/")
def home():
    return {"message": "Server Running"}

@app.post("/generate-house")
def generate_house():

    subprocess.run([
        "blender",
        "--background",
        "--python",
        "generate_house.py"
    ])

    return {
        "model_url": "/output/house.glb"
    }
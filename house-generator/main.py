from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import subprocess

app = FastAPI()

# serve output folder
app.mount("/output", StaticFiles(directory="output"), name="output")

@app.get("/")
def home():
    return {"message": "Server Running"}

@app.post("/generate-house")
def generate_house():

    blender_path = r"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe"

    subprocess.run([
        blender_path,
        "--background",
        "--python",
        "generate_house.py"
    ])

    return {
        "model_url": "http://127.0.0.1:8000/output/house.glb"
    }
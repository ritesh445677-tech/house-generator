from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import subprocess
import os

app = FastAPI()

BASE_URL = "https://house-generator-production.railway.app"

# ====================================================
# OUTPUT FOLDER
# ====================================================

os.makedirs("output", exist_ok=True)

# ====================================================
# STATIC FILES
# ====================================================

app.mount(
    "/output",
    StaticFiles(directory="output"),
    name="output"
)

# ====================================================
# HOME
# ====================================================

@app.get("/")
def home():

    return {
        "message": "Server Running"
    }

# ====================================================
# GENERATE HOUSE
# ====================================================

@app.post("/generate-house")
def generate_house():

    subprocess.run([

        "blender",

        "--background",

        "--python",

        "generate_house.py"

    ])

    return {

        "success": True,

        "model_url":
        f"{BASE_URL}/output/house.glb"
    }
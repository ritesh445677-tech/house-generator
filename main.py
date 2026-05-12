from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles

import subprocess
import shutil
import os

app = FastAPI()

# ====================================================
# BASE URL
# ====================================================

BASE_URL = "https://house-generator-production.railway.app"

# ====================================================
# FOLDERS
# ====================================================

os.makedirs("output", exist_ok=True)

os.makedirs("uploads", exist_ok=True)

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

        "message": "Server Running",

        "status": True
    }

# ====================================================
# TEXT TO 3D HOUSE
# ====================================================

@app.post("/generate-house")
async def generate_house(

    prompt: str = Form(...)
):

    try:

        # remove old file
        old_file = "output/house.glb"

        if os.path.exists(old_file):
            os.remove(old_file)

        # run blender
        subprocess.run([

            "blender",

            "--background",

            "--python",

            "generate_house.py",

            "--",

            prompt

        ])

        # check file generated
        if not os.path.exists(old_file):

            return {

                "success": False,

                "message": "GLB file not generated"
            }

        return {

            "success": True,

            "prompt": prompt,

            "model_url":
            f"{BASE_URL}/output/house.glb"
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }

# ====================================================
# IMAGE TO 3D HOUSE
# ====================================================

@app.post("/generate-house-image")
async def generate_house_image(

    prompt: str = Form(...),

    file: UploadFile = File(...)
):

    try:

        # save image
        image_path = f"uploads/{file.filename}"

        with open(image_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # remove old model
        old_file = "output/house.glb"

        if os.path.exists(old_file):
            os.remove(old_file)

        # run blender
        subprocess.run([

            "blender",

            "--background",

            "--python",

            "generate_house.py",

            "--",

            image_path,

            prompt

        ])

        # check output
        if not os.path.exists(old_file):

            return {

                "success": False,

                "message": "GLB file not generated"
            }

        return {

            "success": True,

            "image": image_path,

            "prompt": prompt,

            "model_url":
            f"{BASE_URL}/output/house.glb"
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }
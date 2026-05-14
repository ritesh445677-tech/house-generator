from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import subprocess
import shutil
import os
import uuid

# ====================================================
# FASTAPI APP
# ====================================================

app = FastAPI()

# ====================================================
# CORS
# ====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====================================================
# BASE URL
# ====================================================

BASE_URL = "https://house-generator-production.railway.app"

# ====================================================
# FOLDERS
# ====================================================

OUTPUT_DIR = "/app/output"
UPLOAD_DIR = "/app/uploads"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ====================================================
# STATIC FILES
# ====================================================

app.mount(
    "/output",
    StaticFiles(directory=OUTPUT_DIR),
    name="output"
)

# ====================================================
# HOME ROUTE
# ====================================================

@app.get("/")
def home():

    return {
        "message": "Server Running",
        "status": True
    }

# ====================================================
# TEXT TO 3D
# ====================================================

@app.post("/generate-house")
async def generate_house(

    prompt: str = Form(...)

):

    try:

        # ==============================================
        # OUTPUT FILE
        # ==============================================

        model_filename = "house.glb"

        output_file = f"{OUTPUT_DIR}/{model_filename}"

        # remove old file
        if os.path.exists(output_file):
            os.remove(output_file)

        # ==============================================
        # RUN BLENDER
        # ==============================================

        result = subprocess.run(

            [
                "blender",
                "--background",
                "--python",
                "generate_house.py",
                "--",
                prompt
            ],

            capture_output=True,
            text=True,
            timeout=300
        )

        # ==============================================
        # DEBUG LOGS
        # ==============================================

        print("BLENDER STDOUT:")
        print(result.stdout)

        print("BLENDER STDERR:")
        print(result.stderr)

        # ==============================================
        # CHECK FILE
        # ==============================================

        if not os.path.exists(output_file):

            return {

                "success": False,

                "message": "GLB file not generated",

                "stdout": result.stdout,

                "stderr": result.stderr
            }

        # ==============================================
        # SUCCESS
        # ==============================================

        return {

            "success": True,

            "prompt": prompt,

            "model_url":
            f"{BASE_URL}/output/{model_filename}"
        }

    except subprocess.TimeoutExpired:

        return {

            "success": False,

            "error": "Blender process timeout"
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }

# ====================================================
# IMAGE TO 3D
# ====================================================

@app.post("/generate-house-image")
async def generate_house_image(

    prompt: str = Form(...),

    file: UploadFile = File(...)

):

    try:

        # ==============================================
        # UNIQUE FILE NAME
        # ==============================================

        ext = file.filename.split(".")[-1]

        unique_name = f"{uuid.uuid4()}.{ext}"

        image_path = f"{UPLOAD_DIR}/{unique_name}"

        # ==============================================
        # SAVE IMAGE
        # ==============================================

        with open(image_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # ==============================================
        # OUTPUT FILE
        # ==============================================

        model_filename = "house.glb"

        output_file = f"{OUTPUT_DIR}/{model_filename}"

        # remove old file
        if os.path.exists(output_file):
            os.remove(output_file)

        # ==============================================
        # RUN BLENDER
        # ==============================================

        result = subprocess.run(

            [
                "blender",
                "--background",
                "--python",
                "generate_house.py",
                "--",
                image_path,
                prompt
            ],

            capture_output=True,
            text=True,
            timeout=300
        )

        # ==============================================
        # DEBUG LOGS
        # ==============================================

        print("BLENDER STDOUT:")
        print(result.stdout)

        print("BLENDER STDERR:")
        print(result.stderr)

        # ==============================================
        # CHECK FILE
        # ==============================================

        if not os.path.exists(output_file):

            return {

                "success": False,

                "message": "GLB file not generated",

                "stdout": result.stdout,

                "stderr": result.stderr
            }

        # ==============================================
        # SUCCESS
        # ==============================================

        return {

            "success": True,

            "image": image_path,

            "prompt": prompt,

            "model_url":
            f"{BASE_URL}/output/{model_filename}"
        }

    except subprocess.TimeoutExpired:

        return {

            "success": False,

            "error": "Blender process timeout"
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }

# ====================================================
# HEALTH CHECK
# ====================================================

@app.get("/health")
def health():

    return {

        "status": "healthy"
    }

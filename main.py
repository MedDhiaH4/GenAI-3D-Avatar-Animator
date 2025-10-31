from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles  # New import
from fastapi.responses import FileResponse   # New import
import json

app = FastAPI()

# --- API Routes ---
# This is our existing API route. It's perfect as-is.
@app.get("/api/get-animation")
async def get_animation_data():
    with open("skeleton_data.json", "r") as f:
        data = json.load(f)
    return data

# --- NEW: Serve the Frontend ---

# This "mounts" the entire 'static' folder onto the URL path "/static"
# This means any file in our 'static' folder (like main.js or avatar.glb)
# can be accessed by the browser at "http://.../static/filename"
app.mount("/static", StaticFiles(directory="static"), name="static")

# This tells FastAPI that when a user goes to the root URL ("/")
# just send them the 'index.html' file as the response.
@app.get("/")
async def read_index():
    return FileResponse('static/index.html')
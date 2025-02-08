import json
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Load data from JSON file (verceljson.json should contain a list of students with names and marks)
with open("verceljson.json", "r") as file:
    data = json.load(file)

# Convert list to dictionary for fast lookups
student_marks = {student["name"]: student["marks"] for student in data}

@app.get("/")
async def root():
    return {"message": "Welcome to the vercel API. Use /api to access data."}


@app.get("/api")
def get_marks(name: list[str] = Query(...)):  # Accepting multiple 'name' query parameters as a list
    # Get marks for each name, defaulting to 0 if not found
    marks = [student_marks.get(n, 0) for n in name]
    # print(marks)
    return {"marks": marks}

# get_marks(student_marks)
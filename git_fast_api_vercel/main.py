import json
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data from JSON file
with open("verceljson.json", "r") as file:
    data = json.load(file)

# Convert list to dictionary for fast lookups
student_marks = {student["name"]: student["marks"] for student in data}

@app.get("/api")
def get_marks(name: list[str] = Query(...)):
    marks = [student_marks.get(n, 0) for n in name]
    return {"marks": marks}

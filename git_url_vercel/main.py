from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
from bs4 import BeautifulSoup

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

WIKI_BASE_URL = "https://en.wikipedia.org/wiki/"

@app.get("/api/outline")
async def get_country_outline(country: str = Query(..., title="Country Name")):
    url = WIKI_BASE_URL + country.replace(" ", "_")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch Wikipedia page"}

    soup = BeautifulSoup(response.text, "html.parser")
    
    markdown_outline = "## Contents\n\n"
    for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        level = int(heading.name[1])  # Extract the number from h1, h2, etc.
        markdown_outline += f"{'#' * level} {heading.text.strip()}\n\n"
    
    return {"country": country, "outline": markdown_outline}


@app.get("/")
async def root():
    return {"message": "Welcome to the vercel API. Use /api to access data."}

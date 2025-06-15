from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import json
import os
from pathlib import Path
from pymongo import MongoClient

from dotenv import load_dotenv

load_dotenv()
MONGO_DB_URI = os.getenv("MONGO_DB_URI")

# MongoDB connection
client = None
db = None

def get_db():
    global client, db
    if client is None:
        client = MongoClient(MONGO_DB_URI)
        db = client["bible_rag_db"]
    return db

# Lifespan handler for FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize MongoDB connection and load data
    db = get_db()
    app.state.DATA = await load_data(db)
    yield
    # Shutdown: Close MongoDB connection
    if client:
        client.close()

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Thematic Bible Visualizer API",
    description="API for accessing biblical themes, books, and their connections",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data directory path
DATA_DIR = Path(__file__).parent / "data"

# Data models
class Theme(BaseModel):
    id: str
    name: str
    description: str
    color: str
    arcColor: str = "#fbbf24"

class Book(BaseModel):
    id: int
    name: str
    testament: str
    category: str

class ThemeConnection(BaseModel):
    bookId: int
    prominence: int
    events: List[str]

class BookInsight(BaseModel):
    overview: str
    key_scriptures: List[str]
    theological_context: str

# Helper function to load JSON data
def load_json_file(filename: str) -> Any:
    """Load JSON data from a file."""
    try:
        filepath = DATA_DIR / filename
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filename} not found in {DATA_DIR}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding {filename}: {e}")
        return None


async def load_books_database(db):
    collection = db["books"]
    books_list = []
    for book in collection.find({}, {"_id": 0}):  # Exclude MongoDB's default _id field
        # Convert testament to lowercase if needed
        book["testament"] = book["testament"].lower()
        books_list.append(book)
  
    return books_list

async def load_data(db) -> Dict[str, Any]:
    """Load all data from various sources."""
    return {
        "themes": load_json_file("themes.json") or [],
        "books": await load_books_database(db) or [],
        "theme_connections": load_json_file("theme_connections.json") or {},
        "book_insights": load_json_file("book_insights.json") or {}
    } 

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred"}
    )

# Health check endpoint
@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint to verify the API is running."""
    return {"status": "healthy"}

# API Endpoints
@app.get("/api/v1/themes", response_model=List[Theme])
async def get_themes(request: Request):
    """Get all biblical themes."""
    return request.app.state.DATA["themes"]

@app.get("/api/v1/books", response_model=List[Book])
async def get_books(request: Request):
    """Get all biblical books."""
    return request.app.state.DATA["books"]

@app.get("/api/v1/themes/{theme_id}/connections", response_model=List[ThemeConnection])
async def get_theme_connections(theme_id: str, request: Request):
    """Get connections for a specific theme."""
    if theme_id not in request.app.state.DATA["theme_connections"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No connections found for theme '{theme_id}'"
        )
    return request.app.state.DATA["theme_connections"][theme_id]

@app.get("/api/v1/books/{book_id}", response_model=Optional[Book])
async def get_book(book_id: int, request: Request):
    """Get a specific book by ID."""
    book = next((b for b in request.app.state.DATA["books"] if b["id"] == book_id), None)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    return book

@app.get("/api/v1/books/{book_id}/insights", response_model=BookInsight)
async def get_book_insights(book_id: int, request: Request):
    """Get insights for a specific book."""
    if str(book_id) not in request.app.state.DATA["book_insights"]:
        book = next((b for b in request.app.state.DATA["books"] if b["id"] == book_id), None)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {book_id} not found"
            )
        return {
            "overview": f"{book['name']} is part of the {book['category']} "
                      f"section of the {book['testament'].title()} Testament.",
            "key_scriptures": [],
            "theological_context": f"Theological insights for {book['name']} would be displayed here."
        }
    return request.app.state.DATA["book_insights"][str(book_id)]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

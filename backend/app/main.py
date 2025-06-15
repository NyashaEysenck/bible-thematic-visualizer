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

# --- Database Loading Functions ---

async def load_themes_database(db):
    """Loads themes from the 'theology' collection in MongoDB."""
    collection = db["theology"]
    themes_list = []
    for doc in collection.find({}, {"_id": 0}):
        themes_list.append({
            "id": doc.get("id"),
            "name": doc.get("concept"),  # Map 'concept' field to 'name'
            "description": doc.get("description"),
            "color": doc.get("color"),
            "arcColor": doc.get("arcColor")
        })
    return themes_list

async def load_books_database(db):
    """Loads books from the 'books' collection in MongoDB."""
    collection = db["books"]
    books_list = []
    for book in collection.find({}, {"_id": 0}):
        book["testament"] = book.get("testament", "").lower()
        books_list.append(book)
    return books_list

async def load_book_insights_database(db):
    """Loads book insights from the 'book_insights' collection in MongoDB."""
    collection = db["book_insights"]
    insights = {}
    for doc in collection.find({}, {"_id": 0}):
        if doc.get("id"):
            insights[str(doc.get("id"))] = {
                "overview": doc.get("overview"),
                "key_scriptures": doc.get("key_scriptures"),
                "theological_context": doc.get("theological_context")
            }
    return insights

async def load_theme_connections_database(db):
    """Loads theme connections from the 'theology' collection in MongoDB."""
    collection = db["theology"]
    connections_map = {}
    # Fetch documents that have both an 'id' and a 'connections' field
    for doc in collection.find({"id": {"$exists": True}, "connections": {"$exists": True}}, {"_id": 0, "id": 1, "connections": 1}):
        theme_id = doc["id"]
        connections_list = doc["connections"]
        connections_map[theme_id] = connections_list
    return connections_map

async def load_data(db) -> Dict[str, Any]:
    """Load all data from various sources with fallbacks to JSON."""
    # Load themes with fallback
    try:
        themes = await load_themes_database(db)
        if not themes: raise ValueError("No themes found in database.")
    except Exception as e:
        print(f"Error loading themes from database: {e}. Falling back to JSON.")
        themes = load_json_file("themes.json") or []

    # Load book insights with fallback
    try:
        book_insights = await load_book_insights_database(db)
        if not book_insights: raise ValueError("No book insights found in database.")
    except Exception as e:
        print(f"Error loading book insights from database: {e}. Falling back to JSON.")
        book_insights = load_json_file("book_insights.json") or {}

    # Load books (add fallback for robustness)
    try:
        books = await load_books_database(db)
        if not books: raise ValueError("No books found in database.")
    except Exception as e:
        print(f"Error loading books from database: {e}. No JSON fallback available.")
        books = []

    # Load theme connections with fallback
    try:
        theme_connections = await load_theme_connections_database(db)
        if not theme_connections: raise ValueError("No theme connections found in database.")
    except Exception as e:
        print(f"Error loading theme connections from database: {e}. Falling back to JSON.")
        theme_connections = load_json_file("theme_connections.json") or {}

    return {
        "themes": themes,
        "books": books,
        "theme_connections": theme_connections,
        "book_insights": book_insights
    }

# --- Exception Handlers ---

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    # For debugging, you might want to log the actual exception `exc`
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred"}
    )

# --- API Endpoints ---

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint to verify the API is running."""
    return {"status": "healthy"}

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
    connections = request.app.state.DATA["theme_connections"].get(theme_id)
    if connections is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No connections found for theme '{theme_id}'"
        )
    return connections

@app.get("/api/v1/books/{book_id}", response_model=Optional[Book])
async def get_book(book_id: int, request: Request):
    """Get a specific book by ID."""
    book = next((b for b in request.app.state.DATA["books"] if b.get("id") == book_id), None)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    return book

@app.get("/api/v1/books/{book_id}/insights", response_model=BookInsight)
async def get_book_insights(book_id: int, request: Request):
    """Get insights for a specific book."""
    insights = request.app.state.DATA["book_insights"].get(str(book_id))
    if not insights:
        book = next((b for b in request.app.state.DATA["books"] if b.get("id") == book_id), None)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {book_id} not found"
            )
        # Return default structure if no specific insight is found
        return {
            "overview": f"{book.get('name')} is part of the {book.get('category')} "
                          f"section of the {book.get('testament', '').title()} Testament.",
            "key_scriptures": [],
            "theological_context": f"Theological insights for {book.get('name')} would be displayed here."
        }
    return insights

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# This module is responsible for loading data from the database and fallback JSON files.

import json
from pathlib import Path
from typing import Any, Dict

DATA_DIR = Path(__file__).parent / "data"

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

async def load_themes_from_db(db):
   """Loads themes from the 'theology' collection in MongoDB."""
   collection = db["theology"]
   themes_list = []
   for doc in collection.find({}, {"_id": 0}):
       themes_list.append({
           "id": doc.get("id"),
           "name": doc.get("concept"),
           "description": doc.get("description"),
           "color": doc.get("color"),
           "arcColor": doc.get("arcColor")
       })
   return themes_list

async def load_books_from_db(db):
   """Loads books from the 'books' collection in MongoDB, ordered by 'id'."""
   collection = db["books"]
   books_list = []
   for book in collection.find({}, {"_id": 0}).sort("id", 1):
       book["testament"] = book.get("testament", "").lower()
       books_list.append(book)
   return books_list

async def load_book_insights_from_db(db):
   """Loads book insights from the 'books' collection in MongoDB."""
   collection = db["books"]
   insights = {}
   for doc in collection.find({}, {"_id": 0}):
       if doc.get("id"):
           insights[str(doc.get("id"))] = {
               "overview": doc.get("overview"),
               "key_scriptures": doc.get("key_scriptures"),
               "theological_context": doc.get("theological_context")
           }
   return insights

async def load_theme_connections_from_db(db):
   """Loads theme connections from the 'theology' collection in MongoDB."""
   collection = db["theology"]
   connections_map = {}
   for doc in collection.find({"id": {"$exists": True}, "connections": {"$exists": True}}, {"_id": 0, "id": 1, "connections": 1}):
       theme_id = doc["id"]
       connections_list = doc["connections"]
       connections_map[theme_id] = connections_list
   return connections_map

async def load_all_data(db) -> Dict[str, Any]:
   """Load all data from various sources with fallbacks to JSON."""
   data = {}
   try:
       data["themes"] = await load_themes_from_db(db)
       if not data["themes"]: raise ValueError("No themes found in database.")
   except Exception as e:
       print(f"Error loading themes from database: {e}. Falling back to JSON.")
       data["themes"] = load_json_file("themes.json") or []

   try:
       data["book_insights"] = await load_book_insights_from_db(db)
       if not data["book_insights"]: raise ValueError("No book insights found in database.")
   except Exception as e:
       print(f"Error loading book insights from database: {e}. Falling back to JSON.")
       data["book_insights"] = load_json_file("book_insights.json") or {}

   try:
       data["books"] = await load_books_from_db(db)
       if not data["books"]: raise ValueError("No books found in database.")
   except Exception as e:
       print(f"Error loading books from database: {e}. No JSON fallback available.")
       data["books"] = []

   try:
       data["theme_connections"] = await load_theme_connections_from_db(db)
       if not data["theme_connections"]: raise ValueError("No theme connections found in database.")
   except Exception as e:
       print(f"Error loading theme connections from database: {e}. Falling back to JSON.")
       data["theme_connections"] = load_json_file("theme_connections.json") or {}

   return data
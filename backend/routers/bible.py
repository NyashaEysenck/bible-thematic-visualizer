
# This router handles endpoints related to biblical books, chapters, and verses.
from fastapi import APIRouter, HTTPException, status, Request
from typing import List, Optional
from database import get_db
from models import Book, BookInsight, ChapterInfo, VerseInfo

router = APIRouter()

@router.get("/api/v1/books", response_model=List[Book])
async def get_books(request: Request):
   """Get all biblical books."""
   return request.app.state.DATA["books"]

@router.get("/api/v1/books/{book_id}", response_model=Optional[Book])
async def get_book(book_id: int, request: Request):
   """Get a specific book by ID."""
   book = next((b for b in request.app.state.DATA["books"] if b.get("id") == book_id), None)
   if not book:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND,
           detail=f"Book with ID {book_id} not found"
       )
   return book

@router.get("/api/v1/books/{book_id}/insights", response_model=BookInsight)
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
       return {
           "overview": f"{book.get('name')} is part of the {book.get('category')} "
                         f"section of the {book.get('testament', '').title()} Testament.",
           "key_scriptures": [],
           "theological_context": f"Theological insights for {book.get('name')} would be displayed here."
       }
   return insights

@router.get("/api/v1/books/{book}/chapters", response_model=List[ChapterInfo])
async def get_book_chapters(book: str):
   """Get all chapters for a specific book from the bible_esv collection."""
   db = get_db()
   collection = db["bible_esv"]
   pipeline = [
       {"$match": {"book": book}},
       {"$group": {
           "_id": {"chapter": "$chapter", "book": "$book"},
           "verseCount": {"$sum": 1}
       }},
       {"$project": {
           "_id": 0,
           "number": "$_id.chapter",
           "verseCount": "$verseCount",
           "book": "$_id.book"
       }},
       {"$sort": {"number": 1}}
   ]
   chapters = list(collection.aggregate(pipeline))
   if not chapters:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND,
           detail=f"No chapters found for book '{book}'"
       )
   return chapters

@router.get("/api/v1/books/{book}/chapters/{chapter_number}/verses", response_model=List[VerseInfo])
async def get_chapter_verses(book: str, chapter_number: int):
   db = get_db()
   collection = db["bible_esv"]
   verses = list(collection.find(
       {"book": book, "chapter": chapter_number},
       {"_id": 0, "verse": 1, "text": 1, "chapter": 1, "book": 1}
   ).sort("verse", 1))
   if not verses:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND,
           detail=f"No verses found for book '{book}', chapter {chapter_number}"
       )
   return verses
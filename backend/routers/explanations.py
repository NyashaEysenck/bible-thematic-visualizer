
# This router manages the AI-powered explanation endpoints.
from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from database import get_db
from models import EventExplanationRequest, EventExplanationResponse, VerseExplanationRequest, VerseExplanationResponse
from ai_services import get_embedding, generate_event_explanation, generate_verse_explanation
from typing import List, Dict

router = APIRouter()

async def vector_search_theology(db, query_embedding: List[float], limit: int = 5) -> List[Dict]:
   """Perform vector search on theology collection."""
   try:
       collection = db["theology"]
       pipeline = [
           {
               "$vectorSearch": {
                   "index": "vector_index",
                   "path": "embedding",
                   "queryVector": query_embedding,
                   "numCandidates": 20,
                   "limit": limit
               }
           },
           {
               "$project": {
                   "_id": 0,
                   "concept": 1,
                   "summary": 1,
                   "description": 1,
                   "score": {"$meta": "vectorSearchScore"}
               }
           }
       ]
       
       results = list(collection.aggregate(pipeline))
       return results
   except Exception as e:
       print(f"Error in theology vector search: {e}")
       return []

async def vector_search_commentary(db, query_embedding: List[float], limit: int = 5) -> List[Dict]:
   """Perform vector search on commentary_chunks collection."""
   try:
       collection = db["commentary_chunks"]
       pipeline = [
           {
               "$vectorSearch": {
                   "index": "vector_index",
                   "path": "embedding",
                   "queryVector": query_embedding,
                   "numCandidates": 20,
                   "limit": limit
               }
           },
           {
               "$project": {
                   "_id": 0,
                   "text": 1,
                   "book": 1,
                   "chapter": 1,
                   "verse": 1,
                   "source": 1,
                   "score": {"$meta": "vectorSearchScore"}
               }
           }
       ]
       
       results = list(collection.aggregate(pipeline))
       return results
   except Exception as e:
       print(f"Error in commentary vector search: {e}")
       return []

async def get_verse_text(db, book: str, chapter: int, verse: int) -> str:
   """Get the actual verse text from bible_esv collection."""
   try:
       collection = db["bible_esv"]
       verse_doc = collection.find_one({
           "book": book,
           "chapter": chapter,
           "verse": verse
       })
       return verse_doc.get("text", "") if verse_doc else ""
   except Exception as e:
       print(f"Error getting verse text: {e}")
       return ""

@router.post("/api/v1/explain-event", response_model=EventExplanationResponse, status_code=status.HTTP_200_OK)
async def explain_event(request: EventExplanationRequest):
   """
   Generate or retrieve an explanation for a biblical event based on book, verse, and theme.
   """
   db = get_db()
   explanations_collection = db["event_explanations"]

   try:
       existing_explanation = explanations_collection.find_one({
           "book": request.book,
           "verse": request.verse,
           "theme": request.theme
       })

       if existing_explanation:
           existing_explanation.pop('_id', None)
           return existing_explanation

       query = f"{request.book} {request.verse} {request.theme}"
       query_embedding = await get_embedding(query)
       
       if not query_embedding:
           raise HTTPException(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail="Failed to generate query embedding"
           )

       theology_results = await vector_search_theology(db, query_embedding, limit=3)
       commentary_results = await vector_search_commentary(db, query_embedding, limit=3)

       explanation = await generate_event_explanation(
           query, theology_results, commentary_results,
           request.book, request.verse, request.theme
       )

       new_explanation = {
           "book": request.book,
           "verse": request.verse,
           "theme": request.theme,
           "explanation": explanation,
           "created_at": datetime.utcnow().isoformat()
       }

       explanations_collection.insert_one(new_explanation.copy())
       new_explanation.pop('_id', None)
       return new_explanation

   except Exception as e:
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail=f"Failed to generate explanation: {str(e)}"
       )

@router.post("/api/v1/explain-verse", response_model=VerseExplanationResponse, status_code=status.HTTP_200_OK)
async def explain_verse(request: VerseExplanationRequest):
   """
   Generate or retrieve an explanation for a specific Bible verse.
   """
   db = get_db()
   verse_explanations = db["verse_explanations"]

   try:
       existing_explanation = verse_explanations.find_one({
           "book": request.book,
           "chapter": request.chapter,
           "verse": request.verse
       })

       if existing_explanation:
           existing_explanation.pop('_id', None)
           return existing_explanation

       verse_text = await get_verse_text(db, request.book, request.chapter, request.verse)
       
       if not verse_text:
           raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail=f"Verse not found: {request.book} {request.chapter}:{request.verse}"
           )

       query = f"{request.book} {request.chapter}:{request.verse} {verse_text}"
       query_embedding = await get_embedding(query)
       
       if not query_embedding:
           raise HTTPException(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail="Failed to generate query embedding"
           )

       theology_results = await vector_search_theology(db, query_embedding, limit=3)
       commentary_results = await vector_search_commentary(db, query_embedding, limit=3)

       explanation = await generate_verse_explanation(
           verse_text, theology_results, commentary_results,
           request.book, request.chapter, request.verse
       )

       new_explanation = {
           "book": request.book,
           "chapter": request.chapter,
           "verse": request.verse,
           "explanation": explanation,
           "created_at": datetime.utcnow().isoformat()
       }

       verse_explanations.insert_one(new_explanation.copy())
       new_explanation.pop('_id', None)
       return new_explanation

   except Exception as e:
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail=f"Failed to generate verse explanation: {str(e)}"
       )

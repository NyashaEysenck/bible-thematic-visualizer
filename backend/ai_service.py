# This module encapsulates all interactions with the Google Generative AI.
import os
import google.generativeai as genai
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

async def get_embedding(text: str) -> List[float]:
   """Generate embedding for text using Google AI."""
   try:
       model = "models/text-embedding-004"
       result = genai.embed_content(model=model, content=text, task_type="retrieval_document")
       return result['embedding']
   except Exception as e:
       print(f"Error generating embedding: {e}")
       return []

async def generate_event_explanation(query: str, theology_context: List[Dict], commentary_context: List[Dict], book: str, verse: str, theme: str) -> str:
   """Generate explanation using Google AI with RAG context."""
   try:
       theology_text = "\n".join([
           f"Concept: {item.get('concept', '')}\nSummary: {item.get('summary', '')}\nDescription: {item.get('description', '')}"
           for item in theology_context
       ])
       
       commentary_text = "\n".join([
           f"Commentary: {item.get('text', '')}"
           for item in commentary_context
       ])
       
       prompt = f"""You are a biblical scholar providing detailed explanations of biblical events and their theological significance.

CONTEXT FROM THEOLOGICAL SOURCES:
{theology_text}

CONTEXT FROM BIBLICAL COMMENTARIES:
{commentary_text}

QUERY: Explain the biblical event in {book} {verse} as it relates to the theme of {theme}.

Please provide a comprehensive explanation that:
1. Describes the specific event or passage
2. Explains its significance within the theme of {theme}
3. Provides historical and cultural context
4. Discusses theological implications
5. Connects it to broader biblical themes and narratives

Keep the explanation scholarly but accessible, approximately 200-300 words."""

       model = genai.GenerativeModel('gemini-1.5-flash')
       response = model.generate_content(prompt)
       
       return response.text if response.text else "Unable to generate explanation at this time."
       
   except Exception as e:
       print(f"Error generating event explanation: {e}")
       return f"Error generating explanation for {book} {verse} related to {theme}."

async def generate_verse_explanation(verse_text: str, theology_context: List[Dict], commentary_context: List[Dict], book: str, chapter: int, verse: int) -> str:
   """Generate verse explanation using Google AI with RAG context."""
   try:
       theology_text = "\n".join([
           f"Concept: {item.get('concept', '')}\nSummary: {item.get('summary', '')}"
           for item in theology_context
       ])
       
       commentary_text = "\n".join([
           f"Commentary: {item.get('text', '')}"
           for item in commentary_context
       ])
       
       prompt = f"""You are a biblical scholar providing detailed explanations of Bible verses.

VERSE TEXT: "{verse_text}"
REFERENCE: {book} {chapter}:{verse}

THEOLOGICAL CONTEXT:
{theology_text}

COMMENTARY CONTEXT:
{commentary_text}

Please provide a comprehensive explanation of this verse that includes:
1. The literal meaning and translation insights
2. Historical and cultural context
3. Theological significance
4. How it fits within the broader context of the chapter/book
5. Practical applications or implications
6. Connections to other relevant biblical passages

Keep the explanation scholarly but accessible, approximately 200-300 words."""

       model = genai.GenerativeModel('gemini-1.5-flash')
       response = model.generate_content(prompt)
       
       return response.text if response.text else "Unable to generate explanation at this time."
       
   except Exception as e:
       print(f"Error generating verse explanation: {e}")
       return f"Error generating explanation for {book} {chapter}:{verse}."


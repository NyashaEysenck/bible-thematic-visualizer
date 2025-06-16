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

       prompt = f"""You are a biblical scholar. Your task is to provide a detailed explanation of a biblical event based on the provided context.

**Topic:** The biblical event in {book} {verse} as it relates to the theme of "{theme}".

**Context from Theological Sources:**
{theology_text}

**Context from Biblical Commentaries:**
{commentary_text}

**Instructions:**
Generate a comprehensive explanation of approximately 200-300 words. The response must be structured with the following headings. Do not use Markdown formatting for the headings, just bold the titles as shown below:

**Event Description:** Briefly describe the specific event or passage.
**Thematic Connection:** Explain its significance specifically within the theme of "{theme}".
**Historical and Cultural Context:** Provide relevant historical and cultural background.
**Theological Implications:** Discuss the key theological takeaways.
**Broader Biblical Narrative:** Connect the event to broader biblical themes and narratives.

Combine these points into a single, cohesive, and scholarly yet accessible explanation.
"""

       model = genai.GenerativeModel('gemini-2.0-flash')
       response = await model.generate_content_async(prompt)

       if response.text:
           # Clean the text to remove unwanted markdown characters before returning
           cleaned_text = response.text.replace('**', '').replace('#', '').strip()
           return cleaned_text
       else:
           return "Unable to generate explanation at this time."


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

       prompt = f"""You are a biblical scholar. Your task is to provide a detailed explanation of a Bible verse based on the provided context.

**Verse for Explanation:** "{verse_text}" ({book} {chapter}:{verse})

**Theological Context:**
{theology_text}

**Commentary Context:**
{commentary_text}

**Instructions:**
Generate a comprehensive explanation of approximately 200-300 words. The response must be structured with the following headings. Do not use Markdown formatting for the headings, just bold the titles as shown below:

**Literal Meaning:** Explain the literal meaning and any key translation insights.
**Historical and Cultural Context:** Describe the relevant historical and cultural background.
**Theological Significance:** Discuss the primary theological message or implication.
**Immediate Context:** Explain how the verse fits within the surrounding chapter and book.
**Practical Application:** Suggest practical applications or implications for the reader.

Combine these points into a single, cohesive, and scholarly yet accessible explanation.
"""

       model = genai.GenerativeModel('gemini-2.0-flash')
       response = await model.generate_content_async(prompt)

       if response.text:
           # Clean the text to remove unwanted markdown characters before returning
           cleaned_text = response.text.replace('**', '').replace('#', '').strip()
           return cleaned_text
       else:
           return "Unable to generate explanation at this time."

   except Exception as e:
       print(f"Error generating verse explanation: {e}")
       return f"Error generating explanation for {book} {chapter}:{verse}."

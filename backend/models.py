# This file contains all the Pydantic data models.
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

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

class ChapterInfo(BaseModel):
   number: int
   verseCount: int
   book: str

class VerseInfo(BaseModel):
   verse: int
   text: str
   chapter: int
   book: str

class EventExplanationRequest(BaseModel):
   book: str
   verse: str
   theme: str

class EventExplanationResponse(BaseModel):
   explanation: str
   book: str
   verse: str
   theme: str
   created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class VerseExplanationRequest(BaseModel):
   book: str
   chapter: int
   verse: int

class VerseExplanationResponse(BaseModel):
   explanation: str
   book: str
   chapter: int
   verse: int
   created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

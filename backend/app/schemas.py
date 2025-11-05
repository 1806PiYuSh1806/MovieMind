# backend/app/schemas.py
from typing import List, Optional
from pydantic import BaseModel

class Movie(BaseModel):
    id: int
    title: str
    year: Optional[int] = None
    genres: List[str] = []
    overview: Optional[str] = None
    posterUrl: Optional[str] = None
    rating: Optional[float] = None

class SearchResponse(BaseModel):
    results: List[Movie]
    total: int
    page: int
    pages: int

class QuizInput(BaseModel):
    genres: List[str] = []
    mood: Optional[str] = None
    pace: Optional[str] = None
    era: Optional[str] = None
    languages: List[str] = []
    min_rating: Optional[float] = None

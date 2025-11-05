# backend/app/main.py
from __future__ import annotations

import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .recommender import MovieRecommender, QuizParams
from .schemas import Movie, SearchResponse, QuizInput
from .utils import default_cors_origins


CSV_PATH = os.environ.get("MOVIES_CSV_PATH", os.path.join(os.path.dirname(__file__), "..", "..", "model", "data.csv"))
recommender = MovieRecommender(csv_path=CSV_PATH)

app = FastAPI(title="Movie Recommender API", version="1.0.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=default_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/api/movies/trending", response_model=list[Movie])
def get_trending(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100)):
    return [Movie(**m) for m in recommender.trending(page=page, page_size=page_size)]

@app.get("/api/movies/{movie_id}", response_model=Movie)
def get_movie(movie_id: int):
    m = recommender.get(movie_id)
    if not m:
        raise HTTPException(status_code=404, detail="Movie not found")
    return Movie(**m)

@app.get("/api/recommend", response_model=list[Movie])
def recommend_for_movie(movie_id: int | None = None, title: str | None = None, top_k: int = Query(10, ge=1, le=50)):
    if movie_id is not None:
        items = recommender.recommend_by_id(movie_id, top_k=top_k)
    elif title:
        items = recommender.recommend_by_title(title, top_k=top_k)
    else:
        raise HTTPException(status_code=400, detail="Provide either movie_id or title")
    return [Movie(**m) for m in items]

@app.get("/api/search", response_model=SearchResponse)
def search(q: str, page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=60)):
    results, total, pages = recommender.search(q=q, page=page, page_size=page_size)
    return SearchResponse(results=[Movie(**m) for m in results], total=total, page=page, pages=pages)

@app.post("/api/recommend/by-quiz", response_model=list[Movie])
def recommend_by_quiz(payload: QuizInput):
    qp = QuizParams(
        genres=payload.genres,
        mood=payload.mood,
        pace=payload.pace,
        era=payload.era,
        languages=payload.languages,
        min_rating=payload.min_rating,
    )
    items = recommender.recommend_by_quiz(qp, top_k=30)
    return [Movie(**m) for m in items]
# backend/app/recommender.py
from __future__ import annotations

import difflib
import math
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


REQUIRED_TEXT_COLS = ['genres', 'keywords', 'tagline', 'cast', 'director']
OPTIONAL_COLS = ['overview', 'year', 'popularity', 'vote_average', 'title', 'original_language', 'runtime', 'release_date']


@dataclass
class QuizParams:
    genres: List[str]
    mood: Optional[str]
    pace: Optional[str]
    era: Optional[str]
    languages: List[str]
    min_rating: Optional[float]


def _safe_year(release_date: Any) -> Optional[int]:
    try:
        dt = pd.to_datetime(release_date, errors="coerce")
        if pd.isna(dt):
            return None
        return int(dt.year)
    except Exception:
        # fallback: string YYYY-...
        s = str(release_date)
        return int(s[:4]) if len(s) >= 4 and s[:4].isdigit() else None


class MovieRecommender:
    """
    TF-IDF recommender based on combined metadata fields.
    Provides: recommend_by_title, recommend_by_id, search, get, trending, recommend_by_quiz.
    """

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df: pd.DataFrame = pd.read_csv(csv_path)

        # Ensure columns exist
        for col in REQUIRED_TEXT_COLS:
            if col not in self.df.columns:
                self.df[col] = ""

        for col in OPTIONAL_COLS:
            if col not in self.df.columns:
                self.df[col] = None

        # Title is mandatory for UX
        if 'title' not in self.df.columns:
            # fall back to original_title if present
            if 'original_title' in self.df.columns:
                self.df['title'] = self.df['original_title'].fillna('Untitled')
            else:
                raise ValueError("CSV must contain a 'title' or 'original_title' column.")

        # Create a stable integer id
        if 'id' in self.df.columns and pd.api.types.is_integer_dtype(self.df['id']):
            self.df['id'] = self.df['id'].astype(int)
        elif 'index' in self.df.columns and pd.api.types.is_integer_dtype(self.df['index']):
            self.df['id'] = self.df['index'].astype(int)
        else:
            self.df = self.df.reset_index(drop=True)
            self.df['id'] = self.df.index.astype(int)

        # Clean NaNs for TF-IDF features
        for feature in REQUIRED_TEXT_COLS:
            self.df[feature] = self.df[feature].fillna('')

        # Combine feature text
        self.df['combined_features'] = (
            self.df['genres'].astype(str) + ' ' +
            self.df['keywords'].astype(str) + ' ' +
            self.df['tagline'].astype(str) + ' ' +
            self.df['cast'].astype(str) + ' ' +
            self.df['director'].astype(str)
        )

        # Vectorize + similarity
        self.vectorizer = TfidfVectorizer()
        self.feature_matrix = self.vectorizer.fit_transform(self.df['combined_features'])
        self.similarity = cosine_similarity(self.feature_matrix)

        # Title lookup
        self.title_to_id = {str(t).strip().lower(): i for t, i in zip(self.df['title'], self.df['id'])}

    # ------------ helpers ------------
    def _row_to_movie(self, row: pd.Series) -> Dict[str, Any]:
        rating = row.get('vote_average', None)
        try:
            rating = float(rating) if rating is not None and not pd.isna(rating) else None
        except Exception:
            rating = None

        year = _safe_year(row.get('release_date', None))

        genres = row.get('genres', "")
        genres_list = [g.strip() for g in str(genres).split('|') if g.strip()] if isinstance(genres, str) else []

        overview = row.get('overview', None)
        overview = None if pd.isna(overview) else str(overview)

        title = str(row.get('title', row.get('original_title', 'Untitled')))

        # Poster placeholder (since your CSV has no poster column)
        from urllib.parse import quote
        poster = f"https://placehold.co/400x600?text={quote(title)}"

        # id
        _id = int(row['id']) if 'id' in row and pd.notna(row['id']) else int(row.name)

        return {
            "id": _id,
            "title": title,
            "year": year,
            "genres": genres_list,
            "overview": overview,
            "posterUrl": poster,
            "rating": rating,
        }

    def _ensure_valid_id(self, movie_id: int) -> bool:
        return int(movie_id) in set(self.df['id'].tolist())

    # ------------ public API ------------
    def get(self, movie_id: int) -> Optional[Dict[str, Any]]:
        if not self._ensure_valid_id(movie_id):
            return None
        row = self.df.loc[self.df['id'] == int(movie_id)].iloc[0]
        return self._row_to_movie(row)

    def trending(self, page: int = 1, page_size: int = 20) -> List[Dict[str, Any]]:
        df = self.df.copy()
        if 'popularity' in df.columns and df['popularity'].notna().any():
            df['_sort'] = pd.to_numeric(df['popularity'], errors='coerce').fillna(0.0)
        elif 'vote_average' in df.columns and df['vote_average'].notna().any():
            df['_sort'] = pd.to_numeric(df['vote_average'], errors='coerce').fillna(0.0)
        else:
            df['_sort'] = 0.0

        df = df.sort_values('_sort', ascending=False)
        start = (page - 1) * page_size
        end = start + page_size
        return [self._row_to_movie(r) for _, r in df.iloc[start:end].iterrows()]

    def recommend_by_id(self, movie_id: int, top_k: int = 10) -> List[Dict[str, Any]]:
        if not self._ensure_valid_id(movie_id):
            return []
        row_idx = self.df.index[self.df['id'] == int(movie_id)][0]
        scores = list(enumerate(self.similarity[row_idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)

        out: List[Dict[str, Any]] = []
        for idx, _score in scores:
            if idx == row_idx:
                continue
            out.append(self._row_to_movie(self.df.iloc[idx]))
            if len(out) >= top_k:
                break
        return out

    def recommend_by_title(self, video_name: str, top_k: int = 10) -> List[Dict[str, Any]]:
        titles = self.df['title'].astype(str).tolist()
        matches = difflib.get_close_matches(video_name, titles, n=1)
        if not matches:
            return []
        title = matches[0]
        movie_id = int(self.df.loc[self.df['title'] == title, 'id'].iloc[0])
        return self.recommend_by_id(movie_id, top_k=top_k)

    def search(self, q: str, page: int = 1, page_size: int = 20) -> Tuple[List[Dict[str, Any]], int, int]:
        q = (q or "").strip()
        if not q:
            return [], 0, 0

        q_vec = self.vectorizer.transform([q])
        sims = cosine_similarity(q_vec, self.feature_matrix).ravel()
        self.df['_sim'] = sims

        title_mask = self.df['title'].astype(str).str.contains(q, case=False, na=False)
        self.df['_boost'] = title_mask.astype(int) * 0.15
        self.df['_score'] = self.df['_sim'] + self.df['_boost']

        ranked = self.df.sort_values('_score', ascending=False)
        total = ranked.shape[0]
        pages = max(1, math.ceil(total / page_size))
        page = max(1, min(page, pages))
        start = (page - 1) * page_size
        end = start + page_size

        results = [self._row_to_movie(r) for _, r in ranked.iloc[start:end].iterrows()]

        self.df.drop(columns=[c for c in ['_sim', '_boost', '_score'] if c in self.df.columns], inplace=True)

        return results, total, pages

    def recommend_by_quiz(self, qp: QuizParams, top_k: int = 30) -> List[Dict[str, Any]]:
        import numpy as np
        df = self.df.copy()

        # hard filters
        if qp.languages:
            df = df[df.get('original_language', '').astype(str).str.lower().isin([l.lower() for l in qp.languages])]

        if qp.min_rating is not None and 'vote_average' in df.columns:
            df = df[pd.to_numeric(df['vote_average'], errors='coerce').fillna(0.0) >= float(qp.min_rating)]

        if 'release_date' in df.columns:
            years = pd.to_datetime(df['release_date'], errors='coerce').dt.year
            df['_year'] = years
            if qp.era == 'classic':          df = df[df['_year'] < 1990]
            elif qp.era == 'nineties':       df = df[(df['_year'] >= 1990) & (df['_year'] < 2000)]
            elif qp.era == 'two_thousands':  df = df[(df['_year'] >= 2000) & (df['_year'] < 2010)]
            elif qp.era == 'tens':           df = df[(df['_year'] >= 2010) & (df['_year'] < 2018)]
            elif qp.era == 'recent':         df = df[df['_year'] >= 2018]

        if qp.pace and 'runtime' in df.columns:
            r = pd.to_numeric(df['runtime'], errors='coerce')
            if qp.pace == 'slow':       df = df[r > 130]
            elif qp.pace == 'moderate': df = df[(r >= 95) & (r <= 130)]
            elif qp.pace == 'fast':     df = df[r < 95]

        if df.empty:
            return []

        mood_map = {
            'uplifting':     ['heartwarming', 'feel-good', 'inspiring'],
            'dark':          ['dark', 'gritty', 'noir', 'tragic'],
            'romantic':      ['romance', 'love', 'relationship'],
            'thrilling':     ['thriller', 'suspense', 'edge-of-seat'],
            'funny':         ['comedy', 'humor', 'hilarious'],
            'mind-bending':  ['mystery', 'twist', 'mind-bending', 'surreal'],
        }

        tokens: List[str] = []
        for g in qp.genres:
            tokens += [g]*3
        if qp.mood and qp.mood in mood_map:
            for t in mood_map[qp.mood]:
                tokens += [t]*2
        era_tokens = {
            'classic': ['classic', 'iconic'],
            'nineties': ['90s'],
            'two_thousands': ['2000s'],
            'tens': ['2010s'],
            'recent': ['recent', 'modern'],
        }
        if qp.era in era_tokens:
            tokens += era_tokens[qp.era]
        for l in qp.languages:
            tokens.append(l)

        if not tokens:
            if 'popularity' in df.columns:
                df = df.sort_values(pd.to_numeric(df['popularity'], errors='coerce').fillna(0.0), ascending=False)
            elif 'vote_average' in df.columns:
                df = df.sort_values(pd.to_numeric(df['vote_average'], errors='coerce').fillna(0.0), ascending=False)
            return [self._row_to_movie(r) for _, r in df.head(top_k).iterrows()]

        query = " ".join(tokens)

        mask = self.df.index.isin(df.index)
        filtered_matrix = self.feature_matrix[mask]
        q_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(q_vec, filtered_matrix).ravel()

        df['_score'] = sims
        v = pd.to_numeric(df.get('vote_average', 0.0), errors='coerce').fillna(0.0)
        p = pd.to_numeric(df.get('popularity', 0.0), errors='coerce').fillna(0.0)
        df['_score2'] = df['_score'] + (v * 0.02) + (p * 0.003)

        ranked = df.sort_values('_score2', ascending=False)
        out = [self._row_to_movie(r) for _, r in ranked.head(top_k).iterrows()]
        for c in ['_score', '_score2', '_year']:
            if c in df.columns:
                df.drop(columns=[c], inplace=True, errors='ignore')
        return out

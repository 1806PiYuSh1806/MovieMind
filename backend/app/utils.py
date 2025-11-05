# backend/app/utils.py
from typing import List

def default_cors_origins() -> List[str]:
    # Vite dev server + common localhosts
    return [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

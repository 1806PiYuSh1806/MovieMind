import { api } from "@/shared/lib/axios";
import type { Movie, SearchResponse } from "./types";

export const MoviesAPI = {
  trending: (page=1) => api.get<Movie[]>("/api/movies/trending", { params:{ page } }).then(r=>r.data),
  byId: (id:string) => api.get<Movie>(`/api/movies/${id}`).then(r=>r.data),
  recommendForMovie: (id:string) => api.get<Movie[]>("/api/recommend", { params:{ movie_id:id } }).then(r=>r.data),
  recommendForUser: (userId:string) => api.get<Movie[]>("/api/recommend/user", { params:{ user_id:userId } }).then(r=>r.data),
  search: (q:string, page=1) => api.get<SearchResponse>("/api/search", { params:{ q, page } }).then(r=>r.data),
  recommendByQuiz: (payload: {
    genres: string[];
    mood?: string | null;
    pace?: string | null;
    era?: string | null;
    languages: string[];
    min_rating?: number | null;
  }) => api.post<Movie[]>("/api/recommend/by-quiz", payload).then(r => r.data),
};

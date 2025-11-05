export type Movie = {
  id: string;
  title: string;
  year?: number;
  genres?: string[];
  overview?: string;
  posterUrl?: string;
  rating?: number; // 0-10
};
export type SearchResponse = { results: Movie[]; total: number; page: number; pages: number; };

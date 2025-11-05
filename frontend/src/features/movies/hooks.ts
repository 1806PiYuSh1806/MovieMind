import { useQuery } from "@tanstack/react-query";
import { MoviesAPI } from "./api";

export const useTrending = (page=1) =>
  useQuery({ queryKey: ["trending", page], queryFn: () => MoviesAPI.trending(page) });

export const useMovie = (id:string) =>
  useQuery({ queryKey: ["movie", id], queryFn: () => MoviesAPI.byId(id), enabled: !!id });

export const useRecommendationsForMovie = (id:string) =>
  useQuery({ queryKey: ["recs", id], queryFn: () => MoviesAPI.recommendForMovie(id), enabled: !!id });

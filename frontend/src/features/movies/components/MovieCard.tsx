import { Link } from "react-router-dom";
import type { Movie } from "../types";
import css from "./MovieCard.module.css";

export default function MovieCard({ movie }: { movie: Movie }){
  return (
    <Link to={`/movie/${movie.id}`} className={css.card}>
      <img
        className={css.thumb}
        src={movie.posterUrl || "/fallback-poster.svg"}
        alt={movie.title}
        onError={(e)=>{ (e.currentTarget as HTMLImageElement).src="/fallback-poster.svg"; }}
      />
      <div className={css.meta}>
        <div className={css.row}>
          <div className={css.title} title={movie.title}>{movie.title}</div>
          {typeof movie.rating === "number" && <span className={css.rating}>{movie.rating.toFixed(1)}</span>}
        </div>
        {movie.year && <div className={css.year}>{movie.year}</div>}
      </div>
    </Link>
  );
}

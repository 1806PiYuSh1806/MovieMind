import { useParams } from "react-router-dom";
import { useMovie, useRecommendationsForMovie } from "@/features/movies/hooks";
import MovieCard from "@/features/movies/components/MovieCard";

export default function MovieDetails(){
  const { id = "" } = useParams();
  const { data: movie, isLoading } = useMovie(id);
  const { data: recs } = useRecommendationsForMovie(id);

  if (isLoading) return <div className="skeleton" style={{height: 200}} />;
  if (!movie) return <div>Not found.</div>;

  return (
    <div className="details" style={{display: "grid", gap: 24, gridTemplateColumns: "minmax(220px, 280px) 1fr"}}>
      <img src={movie.posterUrl || "/fallback-poster.svg"} alt={movie.title} className="card" style={{width: "100%"}} />
      <div>
        <h1 style={{fontSize:"2rem", fontWeight:700, marginBottom:12}}>{movie.title}</h1>
        {movie.year && <p style={{color:"var(--muted)"}}>{movie.year}</p>}
        {movie.overview && <p style={{marginTop:12, lineHeight:1.6, color:"#d4d4d6"}}>{movie.overview}</p>}
      </div>

      {recs && recs.length > 0 && (
        <section style={{gridColumn: "1 / -1"}}>
          <h2 style={{fontSize:"1.2rem", fontWeight:700, margin:"8px 0 12px"}}>Because you watched</h2>
          <div className="grid">
            {recs.map(m => <MovieCard key={m.id} movie={m} />)}
          </div>
        </section>
      )}
    </div>
  );
}

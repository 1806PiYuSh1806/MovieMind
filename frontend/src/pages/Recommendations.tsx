import { useState } from "react";
import { QuizForm, QuizPayload } from "@/features/quiz/QuizForm";
import { MoviesAPI } from "@/features/movies/api";
import MovieCard from "@/features/movies/components/MovieCard";

export default function Recommendations(){
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(payload: QuizPayload){
    setLoading(true); setError(null);
    try {
      const data = await MoviesAPI.recommendByQuiz(payload);
      setResults(data);
    } catch (e:any) {
      setError("Failed to fetch recommendations.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="for-you" style={{display:"grid", gap:16}}>
      <h1 style={{fontSize:"1.6rem", fontWeight:700}}>For You</h1>
      <p style={{color:"var(--muted)"}}>Take a quick taste quiz. We’ll tailor picks immediately.</p>

      <QuizForm onSubmit={handleSubmit} />

      {loading && (
        <div className="grid">
          {Array.from({length:10}).map((_,i)=><div key={i} className="skeleton" style={{height:300}} />)}
        </div>
      )}

      {error && <div style={{color:"#ff6b6b"}}>{error}</div>}

      {results && !loading && (
        <>
          <h2 style={{fontSize:"1.2rem", fontWeight:700}}>Your picks</h2>
          {results.length ? (
            <div className="grid">
              {results.map((m:any)=> <MovieCard key={m.id} movie={m} />)}
            </div>
          ) : (
            <div>No results. Try relaxing filters (rating/era/language).</div>
          )}
        </>
      )}
    </div>
  );
}

import MovieCard from "@/features/movies/components/MovieCard";
import { useTrending } from "@/features/movies/hooks";

export default function Home(){
  const { data, isLoading, error } = useTrending(1);
  if (error) return <div>Failed to load.</div>;

  return (
    <section className="home">
      <h1 style={{fontSize:"1.6rem", fontWeight:700, marginBottom:12}}>Trending</h1>
      <div className="grid">
        {isLoading
          ? Array.from({length: 12}).map((_,i)=>(<div key={i} className="skeleton" style={{height: 300}} />))
          : data?.map(m => <MovieCard key={m.id} movie={m} />)
        }
      </div>
    </section>
  );
}

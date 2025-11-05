import { useEffect, useMemo, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { MoviesAPI } from "@/features/movies/api";
import MovieCard from "@/features/movies/components/MovieCard";

function useQueryParam(name:string){
  const { search } = useLocation();
  return useMemo(()=> new URLSearchParams(search).get(name) || "", [search, name]);
}

export default function SearchResults(){
  const q = useQueryParam("q");
  const navigate = useNavigate();
  const [data, setData] = useState<{results: any[]; total:number; page:number; pages:number} | null>(null);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);

  useEffect(()=>{ setPage(1); }, [q]);

  useEffect(()=>{
    let alive = true;
    if (!q) { setData(null); return; }
    setLoading(true);
    MoviesAPI.search(q, page).then(d => { if(alive) setData(d); }).finally(()=> alive && setLoading(false));
    return ()=>{ alive = false; };
  }, [q, page]);

  if (!q) return <div>Type something to search.</div>;

  return (
    <section>
      <div style={{display:"flex", alignItems:"center", justifyContent:"space-between", marginBottom:12}}>
        <h1 style={{fontSize:"1.2rem", fontWeight:700}}>Results for “{q}”</h1>
        <button className="button" onClick={()=> navigate("/")}>Back</button>
      </div>

      {loading ? (
        <div className="grid">{Array.from({length:10}).map((_,i)=><div key={i} className="skeleton" style={{height:300}} />)}</div>
      ) : data && data.results.length ? (
        <>
          <div className="grid">
            {data.results.map((m:any)=> <MovieCard key={m.id} movie={m} />)}
          </div>
          <div style={{display:"flex", gap:8, justifyContent:"center", marginTop:16}}>
            <button disabled={page<=1} className="button" onClick={()=> setPage(p=>p-1)}>Prev</button>
            <div style={{alignSelf:"center", color:"var(--muted)"}}>{page}/{data.pages}</div>
            <button disabled={page>=data.pages} className="button" onClick={()=> setPage(p=>p+1)}>Next</button>
          </div>
        </>
      ) : (
        <div>No results found.</div>
      )}
    </section>
  );
}

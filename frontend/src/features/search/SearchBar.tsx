import css from "./SearchBar.module.css";
import { useState } from "react";

export function SearchBar({ onSubmit }:{ onSubmit:(query:string)=>void }){
  const [q, setQ] = useState("");
  return (
    <form className={css.form} onSubmit={(e)=>{ e.preventDefault(); onSubmit(q.trim()); }}>
      <input
        className={css.input}
        placeholder="Search movies, titles, genres…"
        value={q}
        onChange={(e)=> setQ(e.target.value)}
      />
    </form>
  );
}

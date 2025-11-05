import { useMemo, useState } from "react";
import css from "./QuizForm.module.css";

const ALL_GENRES = ["Action","Adventure","Animation","Comedy","Crime","Documentary","Drama","Family","Fantasy","History","Horror","Music","Mystery","Romance","Sci-Fi","Thriller","War","Western"];
const MOODS = ["uplifting","dark","romantic","thrilling","funny","mind-bending"] as const;
const PACES = ["slow","moderate","fast"] as const;
const ERAS = [
  { key:"classic", label:"< 1990" },
  { key:"nineties", label:"1990s" },
  { key:"two_thousands", label:"2000s" },
  { key:"tens", label:"2010–2017" },
  { key:"recent", label:"2018+" },
] as const;

export type QuizPayload = {
  genres: string[];
  mood?: string | null;
  pace?: string | null;
  era?: string | null;
  languages: string[];
  min_rating?: number | null;
};

export function QuizForm({ onSubmit }:{ onSubmit:(payload:QuizPayload)=>void }){
  const [genres, setGenres] = useState<string[]>([]);
  const [mood, setMood] = useState<string | null>(null);
  const [pace, setPace] = useState<string | null>(null);
  const [era, setEra] = useState<string | null>(null);
  const [languages, setLanguages] = useState<string[]>(["en"]);
  const [minRating, setMinRating] = useState<number>(7);

  const toggle = (list:string[], v:string) =>
    list.includes(v) ? list.filter(x=>x!==v) : [...list, v];

  return (
    <form className={css.form} onSubmit={(e)=>{ e.preventDefault(); onSubmit({ genres, mood, pace, era, languages, min_rating: minRating }); }}>
      <div className={css.card}>
        <div style={{display:"flex", justifyContent:"space-between", alignItems:"baseline"}}>
          <h3>Pick a few genres</h3>
          <span className={css.help}>{genres.length} selected</span>
        </div>
        <div className={css.row}>
          {ALL_GENRES.map(g => {
            const active = genres.includes(g);
            return (
              <span key={g}
                className={`${css.chip} ${active ? css.chipActive : ""}`}
                onClick={()=> setGenres(prev => toggle(prev,g))}
              >{g}</span>
            );
          })}
        </div>
      </div>

      <div className={css.card}>
        <h3>Mood</h3>
        <div className={css.row}>
          {MOODS.map(m => (
            <span key={m}
              className={`${css.chip} ${mood === m ? css.chipActive : ""}`}
              onClick={()=> setMood(mood === m ? null : m)}
            >{m}</span>
          ))}
        </div>
      </div>

      <div className={css.card}>
        <h3>Pace & Era</h3>
        <div className={css.row}>
          {PACES.map(p => (
            <span key={p}
              className={`${css.chip} ${pace === p ? css.chipActive : ""}`}
              onClick={()=> setPace(pace === p ? null : p)}
            >{p}</span>
          ))}
        </div>
        <div className={css.row} style={{marginTop:8}}>
          {ERAS.map(e => (
            <span key={e.key}
              className={`${css.chip} ${era === e.key ? css.chipActive : ""}`}
              onClick={()=> setEra(era === e.key ? null : e.key)}
            >{e.label}</span>
          ))}
        </div>
      </div>

      <div className={css.card}>
        <h3>Language & Minimum rating</h3>
        <div className={css.row}>
          {["en","hi","es","fr","ko","ja","de","it"].map(l => {
            const active = languages.includes(l);
            return (
              <span key={l}
                className={`${css.chip} ${active ? css.chipActive : ""}`}
                onClick={()=> setLanguages(prev => toggle(prev, l))}
              >{l.toUpperCase()}</span>
            );
          })}
        </div>
        <div style={{marginTop:10}}>
          <label>
            Min rating:
            <input
              type="range" min={0} max={10} step={0.5} value={minRating}
              onChange={(e)=> setMinRating(parseFloat(e.target.value))}
              style={{width:"200px", marginLeft:10}}
            />
            <span style={{marginLeft:8}}>{minRating.toFixed(1)}</span>
          </label>
        </div>
      </div>

      <div className={css.actions}>
        <button type="submit" className="button">Get Recommendations</button>
      </div>
    </form>
  );
}

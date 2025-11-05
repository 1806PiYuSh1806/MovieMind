import { Link, NavLink, useNavigate } from "react-router-dom";
import styles from "./Header.module.css";
import lstyles from "./Layout.module.css";
import { SearchBar } from "@/features/search/SearchBar";

export default function Header(){
  const navigate = useNavigate();
  return (
    <header className={lstyles.header}>
      <div className={`container ${lstyles.row}`}>
        <Link to="/" className={lstyles.brand}>MovieMind</Link>
        <div className={`${styles.searchWrap}`}>
          <SearchBar onSubmit={(q)=> navigate(`/search?q=${encodeURIComponent(q)}`)} />
        </div>
        <nav className={styles.nav}>
          <NavLink to="/" end>Home</NavLink>
          <NavLink to="/recommendations">For You</NavLink>
        </nav>
      </div>
    </header>
  );
}

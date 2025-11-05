import lstyles from "./Layout.module.css";
export default function Footer(){
  return (
    <footer className={lstyles.footer}>
      <div className="container">© {new Date().getFullYear()} MovieMind</div>
    </footer>
  );
}

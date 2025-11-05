export default function RatingStars({ value=0 }:{ value?: number }){
  const full = Math.round(value)/2; // if backend is 0-10, convert roughly to 0-5
  return (
    <div className="wrap">
      {[0,1,2,3,4].map(i => (
        <svg key={i} viewBox="0 0 24 24" className={`star ${i < full ? "" : "dim"}`}>
          <path d="M12 2l3.09 6.26L22 9.27l-5 4.88L18.18 22 12 18.7 5.82 22 7 14.15l-5-4.88 6.91-1.01L12 2z"/>
        </svg>
      ))}
    </div>
  );
}

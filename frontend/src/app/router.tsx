import { createBrowserRouter } from "react-router-dom";
import RootLayout from "./layout/RootLayout";
import Home from "@/pages/Home";
import MovieDetails from "@/pages/MovieDetails";
import Recommendations from "@/pages/Recommendations";
import SearchResults from "@/pages/SearchResults";
import NotFound from "@/pages/NotFound";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    children: [
      { index: true, element: <Home /> },
      { path: "movie/:id", element: <MovieDetails /> },
      { path: "recommendations", element: <Recommendations /> },
      { path: "search", element: <SearchResults /> },
      { path: "*", element: <NotFound /> },
    ],
  },
]);

import { Outlet } from "react-router-dom";
import Header from "./Header";
import Footer from "./Footer";
import lstyles from "./Layout.module.css";

export default function RootLayout(){
  return (
    <>
      <Header />
      <main className={`container ${lstyles.main}`}>
        <Outlet />
      </main>
      <Footer />
    </>
  );
}

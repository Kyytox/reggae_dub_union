import { useState, useContext, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthContext } from "./components/AuthContext";

import SignupPage from "./pages/SignupPage";
import Navbar from "./components/Navbar";
import Home from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import FavorisPage from "./pages/FavorisPage";
import SearchPage from "./pages/SearchPage";
import PageNotFound from "./errors/PageNotFound";

import "./App.css";

function App() {
  const { checkToken } = useContext(AuthContext);

  const check = async () => {
    await checkToken();
  };

  useEffect(() => {
    check();
  }, []);

  return (
    <>
      <Router>
        <div className="App flex flex-col items-center">
          <Navbar />
          <Routes>
            <Route exact path="/" element={<Home />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/favoris" element={<FavorisPage />} />
            <Route path="/search/:search" element={<SearchPage />} />
            <Route path="*" element={<PageNotFound />} />
          </Routes>
        </div>
      </Router>
    </>
  );
}

export default App;

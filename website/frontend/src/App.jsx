import { useState, useContext, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthContext } from "./components/AuthContext";

import SignupPage from "./pages/SignupPage";
import Navbar from "./components/Navbar";
import Home from "./pages/HomePage";
import UniqueShopPage from "./pages/UniqueShopPage";
import UniqueFormatPage from "./pages/UniqueFormatPage";
import LoginPage from "./pages/LoginPage";
import FavorisPage from "./pages/FavorisPage";
import SearchPage from "./pages/SearchPage";
import RandomPage from "./pages/RandomPage";
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
            <Route exact path="/random" element={<RandomPage />} />
            <Route exact path="/shop/:id_shop" element={<UniqueShopPage />} />
            <Route
              exact
              path="/format/:formatName"
              element={<UniqueFormatPage />}
            />
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

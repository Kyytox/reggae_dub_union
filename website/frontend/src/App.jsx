import { useState, useContext, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import { AuthContext } from "./components/AuthContext";
import Signup from "./components/Signup";
import Navbar from "./components/Navbar";
import Home from "./components/Home";
import Login from "./components/Login";
import Favoris from "./components/Favoris";
// import SearchPage from "./components/SearchPage";
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
            <Route path="/signup" element={<Signup />} />
            <Route path="/login" element={<Login />} />
            <Route path="/favoris" element={<Favoris />} />
            {/* <Route */}
            {/*     path="/search/:search" */}
            {/*     element={<SearchPage />} */}
            {/* /> */}
          </Routes>
        </div>
      </Router>
    </>
  );
}

export default App;

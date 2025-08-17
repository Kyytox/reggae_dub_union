import { useContext } from "react";
import { Link } from "react-router-dom";
import { AuthContext } from "./AuthContext";
import SearchBar from "./SearchBar";
import GitHubIcon from "@mui/icons-material/GitHub";
import "./Navbar.css";

function Navbar() {
  const { isLoggedIn, logout } = useContext(AuthContext);

  return (
    <div className="navbar p-1 pr-10 pl-10 mb-3 w-full flex flex-wrap items-center justify-center md:justify-between">
      <div className="navbar_logo flex justify-center w-full md:w-auto">
        <Link to="/">
          <img
            className="navbar_logo mr-4 ml-3 md:ml-0"
            src="/logo.png"
            alt="logo"
            width="50px"
          />
        </Link>
        <a
          href="https://www.facebook.com/association.tunguska/"
          target="_blank"
          style={{
            textDecoration: "none",
            fontSize: "0.7em",
            display: "flex",
            alignItems: "center",
          }}
        >
          Created by <br /> Tunguska Sound System
        </a>
      </div>
      <div className="navbar-items flex flex-wrap items-center justify-center">
        <Link to="/">Home</Link>

        <SearchBar />

        {isLoggedIn ? (
          <>
            <Link to="/favoris">Favoris</Link>
            <Link to="/" onClick={logout}>
              Logout
            </Link>
          </>
        ) : (
          <>
            <Link to="/signup">Sign up</Link>
            <Link to="/login">Login</Link>
          </>
        )}
        <Link to="https://github.com/Kyytox/vinyls_dub_scrap" target="_blank">
          <GitHubIcon />
        </Link>
      </div>
    </div>
  );
}

export default Navbar;

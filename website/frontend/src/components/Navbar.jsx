import { useContext } from "react";
import { Link } from "react-router-dom";
import { AuthContext } from "./AuthContext";
import SearchBar from "./SearchBar";
import "./Navbar.css";

function Navbar() {
    const { isLoggedIn, logout } = useContext(AuthContext);

    return (
        <div className="navbar p-1 pr-10 pl-10 mb-3 w-full flex items-center justify-between">
            <div className="navbar_logo">
                <Link to="/">
                    <img
                        className="navbar_logo mr-4"
                        src="/logo.png"
                        alt="logo"
                        width="50px"
                    />
                </Link>
            </div>
            <div className="navbar_items">
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
            </div>
        </div>
    );
}

export default Navbar;

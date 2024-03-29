import { createContext, useState } from "react";

const AuthContext = createContext();

function AuthProvider(props) {
    const [isLoggedIn, setIsLoggedIn] = useState(() => {
        return sessionStorage.getItem("isLoggedIn") === "true" ? true : false;
    });
    const token = sessionStorage.getItem("token");
    const idUser = sessionStorage.getItem("idUser");

    const login = (idUser, jwtToken) => {
        console.log("login----");
        setIsLoggedIn(true);
        sessionStorage.setItem("idUser", idUser);
        sessionStorage.setItem("token", jwtToken);
        sessionStorage.setItem("isLoggedIn", true);
    };

    const logout = () => {
        setIsLoggedIn(false);
        // setToken(null);
        sessionStorage.removeItem("token");
        sessionStorage.removeItem("idUser");
        sessionStorage.removeItem("isLoggedIn");
    };

    const checkToken = async () => {
        if (token) {
            console.log("checkToken----");
            login(idUser, token);
        } else {
            console.log("checkToken out----");
            logout();
        }
    };

    const value = {
        checkToken,
        isLoggedIn,
        token,
        login,
        logout,
        idUser,
    };

    return <AuthContext.Provider value={value} {...props} />;
}

export { AuthContext, AuthProvider };

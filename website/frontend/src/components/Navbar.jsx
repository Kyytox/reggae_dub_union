import { useContext } from "react";
import React from "react";
import { Link } from "react-router-dom";
import { AuthContext } from "../components/AuthContext";
import SearchBar from "../components/SearchBar";
import GitHubIcon from "@mui/icons-material/GitHub";
import Box from "@mui/material/Box";

import Menu from "@mui/material/Menu";
import Button from "@mui/material/Button";
import Tooltip from "@mui/material/Tooltip";
import MenuItem from "@mui/material/MenuItem";

import "../App.css";

function Navbar() {
  const { isLoggedIn, logout } = useContext(AuthContext);
  const [anchorElShop, setAnchorElShop] = React.useState(null);
  const [anchorElFormat, setAnchorElFormat] = React.useState(null);

  const shops = [
    { name: "jahwaggysrecords", id: 1 },
    { name: "onlyrootsreggae", id: 2 },
    { name: "controltower", id: 3 },
    { name: "pataterecords", id: 4 },
    { name: "lionvibes", id: 5 },
  ];

  const formats = [
    { name: "7", id: 1 },
    { name: "10", id: 2 },
    { name: "12", id: 3 },
    { name: "LP", id: 4 },
    { name: "TEST PRESS", id: 5 },
  ];

  const handleOpenShopMenu = (event) => {
    setAnchorElShop(event.currentTarget);
  };

  const handleCloseShopMenu = () => {
    setAnchorElShop(null);
  };

  const handleOpenFormatMenu = (event) => {
    setAnchorElFormat(event.currentTarget);
  };
  const handleCloseFormatMenu = () => {
    setAnchorElFormat(null);
  };

  return (
    <Box
      className="navbar"
      sx={{
        position: "fixed",
        backgroundColor: "#222222",
        width: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        zIndex: 100,
        padding: { xs: "5px 10px", sm: "5px 20px", md: "5px 30px" },
      }}
    >
      <Link
        to="/"
        style={{
          alignItems: "left",
        }}
      >
        <img
          className="navbar_logo mr-3 ml-0"
          src="/logo.png"
          alt="logo"
          width="50px"
        />
      </Link>
      {/*<a
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
        </a>*/}
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: { xs: 2, sm: 2, md: 3 },
        }}
      >
        <Link to="/" className="hidden sm:inline mr-5">
          Home
        </Link>
        <Link to="/random" className="hidden sm:inline">
          Random
        </Link>

        {/* Menu items Formats */}
        <Box sx={{ flexGrow: 0 }}>
          <Button
            onClick={handleOpenFormatMenu}
            sx={{
              p: 0,
              color: "white",
              textTransform: "none",
              width: "100%",
            }}
          >
            Formats
          </Button>
          <Menu
            sx={{ mt: "45px" }}
            id="menu-appbar"
            anchorEl={anchorElFormat}
            anchorOrigin={{
              vertical: "top",
              horizontal: "right",
            }}
            keepMounted
            transformOrigin={{
              vertical: "top",
              horizontal: "right",
            }}
            open={Boolean(anchorElFormat)}
            onClose={handleCloseFormatMenu}
          >
            {formats.map((item) => (
              <MenuItem key={item.id} onClick={handleCloseFormatMenu}>
                <Link
                  to={`/format/${item.name}`}
                  style={{
                    textDecoration: "none",
                    color: "black",
                    width: "100%",
                  }}
                >
                  {item.name}
                </Link>
              </MenuItem>
            ))}
          </Menu>
        </Box>
        {/* Menu items Formats Shops */}
        <Box sx={{ flexGrow: 0 }}>
          <Button
            onClick={handleOpenShopMenu}
            sx={{ p: 0, color: "white", textTransform: "none" }}
          >
            Shops
          </Button>
          <Menu
            sx={{ mt: "45px" }}
            id="menu-appbar"
            anchorEl={anchorElShop}
            anchorOrigin={{
              vertical: "top",
              horizontal: "right",
            }}
            keepMounted
            transformOrigin={{
              vertical: "top",
              horizontal: "right",
            }}
            open={Boolean(anchorElShop)}
            onClose={handleCloseShopMenu}
          >
            {shops.map((item) => (
              <MenuItem key={item.id} onClick={handleCloseFormatMenu}>
                <Link
                  to={`/shop/${item.id}`}
                  style={{ textDecoration: "none", color: "black" }}
                >
                  {item.name}
                </Link>
              </MenuItem>
            ))}
          </Menu>
        </Box>

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
        <Link
          hidden
          to="https://github.com/Kyytox/vinyls_dub_scrap"
          target="_blank"
        >
          <GitHubIcon />
        </Link>
      </Box>
    </Box>
  );
}

export default Navbar;

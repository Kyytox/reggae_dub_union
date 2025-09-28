import { useContext, useState } from "react";
import { Link } from "react-router-dom";
import { AuthContext } from "../components/AuthContext";
import SearchBar from "../components/SearchBar";
import GitHubIcon from "@mui/icons-material/GitHub";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

import Menu from "@mui/material/Menu";
import Button from "@mui/material/Button";
import MenuItem from "@mui/material/MenuItem";

import "../App.css";

function Navbar() {
  const { isLoggedIn, logout } = useContext(AuthContext);
  const [anchorElShop, setAnchorElShop] = useState(null);
  const [anchorElFormat, setAnchorElFormat] = useState(null);

  const shops = [
    { name: "Jah Waggys Records", id: 1 },
    { name: "OnlyRoots Reggae", id: 2 },
    { name: "Control Tower Records", id: 3 },
    { name: "Patate Records", id: 5 },
    { name: "Lion Vibes", id: 6 },
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
        flexWrap: { xs: "wrap", md: "nowrap" },
        alignItems: "center",
        justifyContent: { xs: "space-around", md: "space-between" },
        zIndex: 100,
        padding: {
          xs: "5px 10px",
          sm: "5px 10px",
          md: "5px 10px",
          lg: "5px 25px",
        },
      }}
    >
      {/*
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
        </a>*/}
      <Typography
        variant="h5"
        component="div"
        sx={{
          color: "white",
          fontWeight: "bold",
          letterSpacing: ".1rem",
          textDecoration: "none",
        }}
      >
        <Link to="/" style={{ textDecoration: "none", color: "white" }}>
          Reggae Dub Union
        </Link>
      </Typography>
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          flexWrap: "wrap",
          gap: { xs: 0, lg: 2 },
        }}
      >
        <Button>
          <Link to="/">Home</Link>
        </Button>
        <Button>
          <Link to="/random">Random</Link>
        </Button>

        {/* Menu items Formats */}
        <Box sx={{ flexGrow: 0 }}>
          <Button onClick={handleOpenFormatMenu} sx={{ color: "white" }}>
            Formats
          </Button>
          <Menu
            id="menu-appbar"
            anchorEl={anchorElFormat}
            anchorOrigin={{
              vertical: "bottom",
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
          <Button onClick={handleOpenShopMenu} aria-controls="menu-appbar">
            Shops
          </Button>
          <Menu
            id="menu-appbar"
            anchorEl={anchorElShop}
            anchorOrigin={{
              vertical: "bottom",
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
            <Button>
              <Link to="/favoris">Favoris</Link>
            </Button>
            <Button>
              <Link to="/" onClick={logout}>
                Logout
              </Link>
            </Button>
          </>
        ) : (
          <>
            <Button>
              <Link to="/login">Login</Link>
            </Button>
            <Button>
              <Link to="/signup">Sign up</Link>
            </Button>
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

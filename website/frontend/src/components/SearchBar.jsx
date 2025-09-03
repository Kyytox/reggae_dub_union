import React, { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";

import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";

import { Search } from "@mui/icons-material";

function SearchBar() {
  const navigate = useNavigate();
  const [search, setSearch] = useState("");

  const handleSearch = (event) => {
    if (event.key === "Enter") {
      navigate("/search/" + search);
    }
  };

  // #test if search is not empty
  const SearchClick = () => {
    if (search !== "") {
      navigate("/search/" + search);
    }
  };

  return (
    <Box
      sx={{
        margin: { xs: "0 10px 0 0", sm: "0 20px 0 0", md: "0 25px 0 1px" },
        width: { xs: "170px", sm: "200px", md: "250px", lg: "300px" },
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <TextField
        id="outlined-basic"
        className="searchBar"
        label="Search"
        variant="outlined"
        size="small"
        value={search}
        onChange={(event) => setSearch(event.target.value)}
        onKeyDown={handleSearch}
      />
      <Button
        size="medium"
        onClick={SearchClick}
        sx={{ minWidth: "0px", paddingLeft: "10px", paddingRight: "5px" }}
      >
        <Search
          sx={{
            color: "white",
          }}
        />
      </Button>
    </Box>
  );
}

export default SearchBar;

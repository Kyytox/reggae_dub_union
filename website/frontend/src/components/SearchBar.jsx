import React, { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "./AuthContext";
import { getAxios } from "./UtilsAxios";

import TextField from "@mui/material/TextField";

function SearchBar() {
  const navigate = useNavigate();
  const [search, setSearch] = useState("");

  const handleSearch = (event) => {
    if (event.key === "Enter") {
      navigate("/search/" + search);
    }
  };

  return (
    <TextField
      id="outlined-basic"
      className="searchBar"
      label="Search"
      variant="outlined"
      size="small"
      value={search}
      onChange={(event) => setSearch(event.target.value)}
      onKeyDown={handleSearch}
      sx={{
        margin: "0 50px 0 20px",
      }}
    />
  );
}

export default SearchBar;

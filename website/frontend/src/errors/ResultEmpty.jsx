import HeadPage from "../components/HeadPage";
import Box from "@mui/material/Box";
import "../App.css";

// composant for Result Empty
function ResultEmpty() {
  return (
    <Box className="main-content-noresults">
      <HeadPage
        text={"No Results Found for your search... "}
        totalVinyls={null}
      />

      <Box
        className="result-empty"
        style={{ marginTop: "5em", width: "100%", textAlign: "center" }}
      ></Box>
    </Box>
  );
}

export default ResultEmpty;

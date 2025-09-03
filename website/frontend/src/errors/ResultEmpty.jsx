import HeadPage from "../components/HeadPage";
import Box from "@mui/material/Box";
import "../App.css";

// composant for Result Empty
function ResultEmpty() {
  return (
    <Box
      className="main-content-noresults"
      sx={{
        justifyContent: "center",
        marginTop: { xs: "200px", md: "150px", lg: "150px" },
      }}
    >
      <HeadPage
        text={"No Results Found for your search... "}
        totalVinyls={null}
      />
    </Box>
  );
}

export default ResultEmpty;

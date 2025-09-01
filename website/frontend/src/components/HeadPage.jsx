import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

import "../App.css";

function HeadPage({ text, totalVinyls }) {
  return (
    <Box
      className="headpage"
      sx={{
        width: "100% ",
        display: "flex",
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "space-between",
        marginBottom: "15px",
      }}
    >
      <Typography variant="h5" sx={{ marginLeft: "40px" }}>
        {text}
      </Typography>
      <Typography variant="body1" sx={{ marginRight: "40px" }}>
        {totalVinyls !== null ? `${totalVinyls} vinyls found` : ""}
      </Typography>
    </Box>
  );
}

export default HeadPage;

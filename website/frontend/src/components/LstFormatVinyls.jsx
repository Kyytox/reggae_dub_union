import { useState } from "react";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import "../App.css";

function LstFormatVinyls({
  lstFormatVinyls,
  lstFormatVinylsSelected,
  setLstFormatVinylsSelected,
}) {
  // change the list of selected format vinyls
  const changeSelectedFormatVinyls = (formatVinyl) => {
    if (lstFormatVinylsSelected.includes(formatVinyl)) {
      const newArray = lstFormatVinylsSelected.filter((e) => e !== formatVinyl);
      setLstFormatVinylsSelected(newArray);
    } else {
      // add it in array
      setLstFormatVinylsSelected([...lstFormatVinylsSelected, formatVinyl]);
    }
  };
  console.log("lstFormatVinylsSelected", lstFormatVinylsSelected);

  return (
    <Box sx={{ "& button": { m: 0.5 } }} className="container-lstFormats">
      {lstFormatVinyls.map((format, key) => (
        <Button
          key={key}
          variant={
            lstFormatVinylsSelected.length === 0
              ? "contained"
              : lstFormatVinylsSelected.some((s) => s === format)
                ? "contained"
                : "outlined"
          }
          onClick={() => changeSelectedFormatVinyls(format)}
          size="small"
          color="primary"
        >
          {format}
        </Button>
      ))}
    </Box>
  );
}

export default LstFormatVinyls;

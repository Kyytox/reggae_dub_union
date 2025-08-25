import * as React from "react";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormControl from "@mui/material/FormControl";
import "../App.css";

function SectionFilter({
  fetchData,
  lstShops,
  lstShopsSelected,
  setLstShopsSelected,
  lstFormatVinyls,
  lstFormatVinylsSelected,
  setLstFormatVinylsSelected,
}) {
  const [value, setValue] = React.useState("DateAdd");

  const handleChange = (event) => {
    setValue(event.target.value);
  };

  // change the list of selected
  const changeSelectedItems = (val, sectionName) => {
    let lstItemsSelected, setLstItemsSelected;
    if (sectionName === "Shops") {
      lstItemsSelected = lstShopsSelected;
      setLstItemsSelected = setLstShopsSelected;
    } else {
      lstItemsSelected = lstFormatVinylsSelected;
      setLstItemsSelected = setLstFormatVinylsSelected;
    }
    if (lstItemsSelected.includes(val)) {
      const newArray = lstItemsSelected.filter((e) => e !== val);
      setLstItemsSelected(newArray);
    } else {
      // add it in array
      setLstItemsSelected([...lstItemsSelected, val]);
    }
  };

  return (
    <div className="container-sectionFilter mt-4 mb-4 flex flex-column items-center justify-center gap-6">
      <Box
        sx={{
          fontWeight: "bold",
          display: "flex",
          flexDirection: "column",
          alignItems: "end",
        }}
      >
        <Box sx={{ "& button": { m: 0.5 } }} className="container-lstSection">
          {lstFormatVinyls.map((item) => {
            const value = item;
            const displayText = item;

            // is the item selected
            const isSelected = lstFormatVinylsSelected.includes(value);

            // if no item selected, all are selected (variant contained)
            const variant =
              lstFormatVinylsSelected.length === 0 || isSelected
                ? "contained"
                : "outlined";
            return (
              <Button
                key={value}
                variant={variant}
                onClick={() => changeSelectedItems(value, "Formats")}
                size="small"
                color="primary"
              >
                {displayText}
              </Button>
            );
          })}
        </Box>
        <Box sx={{ "& button": { m: 0.5 } }} className="container-lstSection">
          {lstShops.map((item) => {
            const value = item.shop_id;
            const displayText = item.shop_name;

            // is the item selected
            const isSelected = lstShopsSelected.includes(value);

            // if no item selected, all are selected (variant contained)
            const variant =
              lstShopsSelected.length === 0 || isSelected
                ? "contained"
                : "outlined";
            return (
              <Button
                key={value}
                variant={variant}
                onClick={() => changeSelectedItems(value, "Shops")}
                size="small"
                color="primary"
              >
                {displayText}
              </Button>
            );
          })}
        </Box>
      </Box>

      <FormControl>
        <RadioGroup
          aria-labelledby="controlled-radio-buttons-group"
          name="controlled-radio-buttons-group"
          value={value}
          onChange={handleChange}
        >
          <FormControlLabel
            value="DateAdd"
            control={<Radio />}
            label="Date Added"
          />
          <FormControlLabel value="Random" control={<Radio />} label="Random" />
        </RadioGroup>
      </FormControl>

      <Button
        variant="text"
        onClick={() => {
          fetchData();
        }}
      >
        Apply Filters
      </Button>
    </div>
  );
}

export default SectionFilter;

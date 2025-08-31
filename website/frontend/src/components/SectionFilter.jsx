import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Chip from "@mui/material/Chip";
import "../App.css";

function SectionFilter({
  clickApplyFilters,
  lstShops,
  lstShopsSelected,
  setLstShopsSelected,
  lstFormats,
  lstFormatsSelected,
  setLstFormatsSelected,
}) {
  // change the list of selected
  const changeSelectedItems = (val, sectionName) => {
    let lstItemsSelected, setLstItemsSelected;
    if (sectionName === "Shops") {
      lstItemsSelected = lstShopsSelected;
      setLstItemsSelected = setLstShopsSelected;
    } else {
      lstItemsSelected = lstFormatsSelected;
      setLstItemsSelected = setLstFormatsSelected;
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
    <Box
      className="container-sectionFilter left-0 fixed"
      sx={{
        width: { xs: "100%", md: "12%", lg: "12%", xl: "12%" },
        display: "flex",
        flexDirection: "row",
        alignItems: "center",
        flexWrap: "wrap",
        p: 2,
        ml: 1,
        gap: 3,
      }}
    >
      {lstFormats && (
        <Box className="container-lstSection">
          <Typography sx={{ marginLeft: "5px", textAlign: "left" }}>
            Formats:
          </Typography>
          <Box
            sx={{
              display: "flex",
              flexDirection: "row",
              flexWrap: "wrap",
              gap: 1,
            }}
          >
            {lstFormats.map((item) => {
              const value = item;
              const displayText = item;

              // is the item selected
              const isSelected = lstFormatsSelected.includes(value);

              // if no item selected, all are selected (variant contained)
              const variant = isSelected ? "contained" : "outlined";
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
        </Box>
      )}
      {lstShops && (
        <Box className="container-lstSection">
          <Typography
            sx={{
              marginLeft: "5px",
              textAlign: "left",
            }}
          >
            Shops:
          </Typography>
          <Box
            sx={{
              display: "flex",
              flexDirection: "row",
              flexWrap: "wrap",
              gap: 1,
            }}
          >
            {lstShops.map((item) => {
              const value = item.shop_id;
              const displayText = item.shop_name;

              // is the item selected
              const isSelected = lstShopsSelected.includes(value);

              // if no item selected, all are selected (variant contained)
              const variant = isSelected ? "contained" : "outlined";
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
      )}

      {/* Order By Radio Buttons 
      <FormControl>
        <Typography sx={{ marginLeft: "5px", textAlign: "left" }}>
          Order By:
        </Typography>
        <RadioGroup
          row
          aria-labelledby="controlled-radio-buttons-group"
          name="controlled-radio-buttons-group"
          value={orderBy}
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
      */}

      <Button
        variant="text"
        color="secondary"
        onClick={() => {
          clickApplyFilters();
        }}
      >
        Apply Filters
      </Button>
    </Box>
  );
}

export default SectionFilter;

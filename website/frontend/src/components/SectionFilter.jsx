import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import "../App.css";

function SectionFilter({
  lstItems,
  lstItemsSelected,
  setLstItemsSelected,
  sectionName,
}) {
  // change the list of selected
  const changeSelectedItems = (val) => {
    // const val = sectionName === "Shops" ? item.shop_id : item;

    if (lstItemsSelected.includes(val)) {
      const newArray = lstItemsSelected.filter((e) => e !== val);
      setLstItemsSelected(newArray);
    } else {
      // add it in array
      setLstItemsSelected([...lstItemsSelected, val]);
    }
  };

  return (
    <Box sx={{ "& button": { m: 0.5 } }} className="container-lstSection">
      {lstItems.map((item) => {
        const value = sectionName === "Shops" ? item.shop_id : item;
        const displayText = sectionName === "Shops" ? item.shop_name : item;

        // is the item selected
        const isSelected = lstItemsSelected.includes(value);

        // if no item selected, all are selected (variant contained)
        const variant =
          lstItemsSelected.length === 0 || isSelected
            ? "contained"
            : "outlined";

        return (
          <Button
            key={value}
            variant={variant}
            onClick={() => changeSelectedItems(value)}
            size="small"
            color="primary"
          >
            {displayText}
          </Button>
        );
      })}
    </Box>
  );
}

export default SectionFilter;

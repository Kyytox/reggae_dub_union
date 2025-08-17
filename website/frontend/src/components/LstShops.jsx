import { useState } from "react";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import "../App.css";

function LstShops({ lstShops, lstShopsSelected, setLstShopsSelected }) {
  // change the list of selected shops
  const changeSelectedShops = (shop) => {
    if (lstShopsSelected.includes(shop.shop_name)) {
      const newArray = lstShopsSelected.filter((e) => e !== shop.shop_name);
      setLstShopsSelected(newArray);
    } else {
      // add it in array
      setLstShopsSelected([...lstShopsSelected, shop.shop_name]);
    }
  };

  return (
    <Box sx={{ "& button": { m: 0.5 } }} className="container-lstShops">
      {lstShops.map((shop, key) => (
        <Button
          key={key}
          variant={
            lstShopsSelected.length === 0
              ? "contained"
              : lstShopsSelected.some((s) => s === shop.shop_name)
                ? "contained"
                : "outlined"
          }
          size="small"
          color="primary"
          onClick={() => changeSelectedShops(shop)}
        >
          {shop.shop_name}
        </Button>
      ))}
    </Box>
  );
}

export default LstShops;

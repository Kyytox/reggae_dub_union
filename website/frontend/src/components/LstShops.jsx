import { useState } from "react";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import "../App.css";

function LstShops({ lstShops, lstShopsSelected, setLstShopsSelected }) {
    // change the list of selected shops
    const changeSelectedShops = (shop) => {
        if (lstShopsSelected.includes(shop.name)) {
            const newArray = lstShopsSelected.filter((e) => e !== shop.name);
            setLstShopsSelected(newArray);
        } else {
            // add it in array
            setLstShopsSelected([...lstShopsSelected, shop.name]);
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
                            : lstShopsSelected.some((s) => s === shop.name)
                            ? "contained"
                            : "outlined"
                    }
                    size="small"
                    color="primary"
                    onClick={() => changeSelectedShops(shop)}
                >
                    {shop.name}
                </Button>
            ))}
        </Box>
    );
}

export default LstShops;

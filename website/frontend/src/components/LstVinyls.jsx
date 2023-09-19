import { useContext, useEffect, useState, useRef, useCallback } from "react";
import { AuthContext } from "./AuthContext";
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import FavoriteIcon from "@mui/icons-material/Favorite";
import FavoriteBorderIcon from "@mui/icons-material/FavoriteBorder";
import ShoppingCartCheckoutIcon from "@mui/icons-material/ShoppingCartCheckout";
import InfiniteScroll from "react-infinite-scroll-component";
import { Button, CardActionArea, CardActions } from "@mui/material";
import { postAxiosAuth } from "./UtilsAxios";

import "../App.css";

function LstVinyls({
    lstVinyls,
    playSong,
    songPlaying,
    lstFavoris,
    setLstFavoris,
    loadMoreData,
}) {
    const { isLoggedIn, idUser } = useContext(AuthContext);

    // Add Favoris
    const toggleFavori = async (vinyl) => {
        const data = {
            id_user: idUser,
            id_vinyl: vinyl.song_id_vinyl,
            id_song: vinyl.song_id,
        };

        const result = await postAxiosAuth("/toggle_favori", data);

        if (result.message === "create") {
            setLstFavoris([...lstFavoris, vinyl]);
        } else {
            setLstFavoris(lstFavoris.filter((favori) => favori !== vinyl));
        }
    };

    return (
        <div className="container-lstVinyls">
            <InfiniteScroll
                dataLength={lstVinyls.length}
                next={loadMoreData}
                hasMore={true}
                loader={<h4>Loading...</h4>}
                endMessage={
                    <p style={{ textAlign: "center" }}>
                        <b>Yay! You have seen it all</b>
                    </p>
                }
            >
                <Grid
                    container
                    display="flex"
                    direction="row"
                    justifyContent="center"
                    alignItems="center"
                    paddingLeft={{ xs: 0, md: 3, xl: 8 }}
                    paddingRight={{ xs: 0, md: 3, xl: 8 }}
                    spacing={{ xs: 1, md: 4 }}
                    columns={{ xs: 4, sm: 6, md: 8, lg: 10, xl: 12 }}
                >
                    {lstVinyls.map((vinyl, key) => (
                        <Grid item xs={2} sm={2} md={2} key={key}>
                            <Card
                                sx={{
                                    maxWidth: {
                                        xs: 180,
                                        sm: 230,
                                        md: 240,
                                        lg: 240,
                                    },
                                    minWidth: {
                                        xs: 180,
                                        sm: 230,
                                        md: 240,
                                        lg: 240,
                                    },
                                    maxHeight: {
                                        xs: 350,
                                        sm: 310,
                                        md: 300,
                                        lg: 300,
                                    },
                                    backgroundColor:
                                        songPlaying === vinyl
                                            ? "#4b4a4a"
                                            : "#18181b",
                                    minHeight: 300,
                                    display: "flex",
                                    flexDirection: "column",
                                    justifyContent: "start",
                                }}
                            >
                                <CardActions
                                    sx={{
                                        padding: 0.5,
                                    }}
                                >
                                    {isLoggedIn ? (
                                        <Button
                                            size="small"
                                            color="primary"
                                            onClick={() => toggleFavori(vinyl)}
                                        >
                                            {lstFavoris.some(
                                                (favori) =>
                                                    favori.song_id ===
                                                    vinyl.song_id
                                            ) ? (
                                                <FavoriteIcon />
                                            ) : (
                                                <FavoriteBorderIcon />
                                            )}
                                        </Button>
                                    ) : (
                                        <p style={{ display: "none" }}></p>
                                    )}

                                    <Typography
                                        variant="caption"
                                        color="#989898"
                                        sx={isLoggedIn ? {} : { ml: "1em" }}
                                    >
                                        {vinyl.site}
                                    </Typography>
                                    <Button
                                        size="small"
                                        color="primary"
                                        href={vinyl.url}
                                        target="_blank"
                                    >
                                        <ShoppingCartCheckoutIcon />
                                    </Button>
                                </CardActions>
                                <CardActionArea
                                    onClick={() => playSong(vinyl)}
                                    sx={{
                                        display: "flex",
                                        flexDirection: "column",
                                        justifyContent: "space-between",
                                        height: "100%",
                                    }}
                                >
                                    <CardMedia
                                        component="img"
                                        image={
                                            vinyl.image || "/vinyl_neutral.png"
                                        }
                                        alt={vinyl.title}
                                        onError={(e) => {
                                            e.target.src = "/vinyl_neutral.png";
                                        }}
                                        sx={{
                                            height: "130px",
                                            width: "130px",
                                            borderRadius: 50,
                                        }}
                                    />
                                    <CardContent
                                        sx={{
                                            padding: 0.5,
                                            height: "8em",
                                            display: "flex",
                                            flexDirection: "column",
                                            justifyContent: "space-evenly",
                                        }}
                                    >
                                        <Typography
                                            gutterBottom
                                            variant="subtitle2"
                                            component="div"
                                            color="white"
                                        >
                                            {vinyl.title}
                                        </Typography>
                                        <Typography
                                            gutterBottom
                                            variant="subtitle2"
                                            component="div"
                                            color="#b7b7b7"
                                        >
                                            {vinyl.song_title}
                                        </Typography>
                                    </CardContent>
                                </CardActionArea>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
            </InfiniteScroll>
        </div>
    );
}

export default LstVinyls;

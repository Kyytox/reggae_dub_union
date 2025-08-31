import { useContext, useEffect, useState, useRef, useCallback } from "react";
import * as React from "react";
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
import { styled } from "@mui/material/styles";
import Collapse from "@mui/material/Collapse";
import IconButton from "@mui/material/IconButton";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import PauseIcon from "@mui/icons-material/Pause";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import CircularProgress from "@mui/material/CircularProgress";
import Box from "@mui/material/Box";

import { postAxiosAuth } from "../requests/UtilsAxios";
import { AuthContext } from "./AuthContext";

import "../App.css";

const StyledCardActionArea = styled(CardActionArea)(
  ({ theme }) => `
    .MuiCardActionArea-focusHighlight {
        background: transparent;
    }
`,
);

const ExpandMore = styled((props) => {
  const { expand, ...other } = props;
  return <IconButton {...other} />;
})(({ theme, expand }) => ({
  marginLeft: "auto",
  color: "white",
  transition: theme.transitions.create("transform", {
    duration: theme.transitions.duration.shortest,
  }),
  transform: expand ? "rotate(0deg)" : "rotate(180deg)",
}));

function SectionVinyls({
  lstSongs,
  lstVinyls,
  playSong,
  songPlaying,
  lstFavoris,
  setLstFavoris,
  loadMoreData,
  topLoadMore,
}) {
  const { isLoggedIn, idUser } = useContext(AuthContext);

  // State to manage expanded states of vinyls
  const [expandedStates, setExpandedStates] = React.useState({});
  const handleExpandClick = (vinylId) => {
    setExpandedStates((prev) => ({
      ...prev,
      [vinylId]: !prev[vinylId],
    }));
  };

  // Add Favoris
  const toggleFavori = async (vinyl) => {
    const data = {
      user_id: idUser,
      vinyl_id: vinyl.vinyl_id,
    };

    const result = await postAxiosAuth("/toggle_favori", data);

    if (result.message === "create") {
      setLstFavoris([...lstFavoris, vinyl]);
    } else {
      setLstFavoris(
        lstFavoris.filter((favori) => favori.vinyl_id !== vinyl.vinyl_id),
      );
    }
  };

  return (
    <Box sx={{ flexGrow: 1, marginLeft: { xs: 0, sm: 2, md: "13%" } }}>
      <InfiniteScroll
        dataLength={lstVinyls.length}
        next={loadMoreData}
        hasMore={topLoadMore}
        loader={
          <Box
            sx={{
              alignItems: "center",
              display: "flex",
              justifyContent: "center",
              padding: 2,
              marginTop: 5,
            }}
          >
            <CircularProgress />
          </Box>
        }
        // endMessage={
        //   <p style={{ textAlign: "center" }}>
        //     <b>Yay! You have seen it all</b>
        //   </p>
        // }
      >
        <Grid
          container
          sx={{
            // justifyContent: "space-evenly",
            justifyContent: "center",
            alignItems: "flex-start",
            gap: 2,
          }}
        >
          {lstVinyls.map((vinyl, key) => (
            <Grid key={key}>
              <Card
                sx={{
                  width: { xs: 200, sm: 220, md: 240 },
                  backgroundColor:
                    songPlaying && songPlaying.vinyl_id === vinyl.vinyl_id
                      ? "#3a3a3a"
                      : "#18181b",
                  color: "white",
                  height: 330,
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "space-between",
                  transition: "background-color 0.3s ease",
                  "&:hover": {
                    backgroundColor: "#3a3a3a",
                  },
                }}
              >
                <Collapse
                  in={!expandedStates[vinyl.vinyl_id]}
                  timeout={300}
                  unmountOnExit
                >
                  <StyledCardActionArea
                    onClick={() =>
                      playSong(
                        lstSongs.find(
                          (song) => song.vinyl_id === vinyl.vinyl_id,
                        ),
                      )
                    }
                    sx={{
                      display: "flex",
                      flexDirection: "column",
                      justifyContent: "start",
                      height: "auto",
                      padding: 2,
                    }}
                  >
                    <CardMedia
                      component="img"
                      image={vinyl.vinyl_image || "/vinyl_neutral.png"}
                      alt={vinyl.vinyl_title}
                      onError={(e) => {
                        e.target.src = "/vinyl_neutral.png";
                      }}
                      sx={{
                        height: "130px",
                        width: "130px",
                      }}
                    />
                    <CardContent
                      sx={{
                        padding: 0.5,
                        height: "8em",
                        flexGrow: 1,
                        display: "flex",
                        flexDirection: "column",
                        justifyContent: "start",
                      }}
                    >
                      {/* Shop name */}
                      <Typography
                        variant="caption"
                        color="#989898"
                        sx={isLoggedIn ? {} : { ml: "1em" }}
                      >
                        {vinyl.shop_name}
                      </Typography>

                      {/* Format */}
                      <Typography
                        variant="caption"
                        color="#989898"
                        sx={isLoggedIn ? {} : { ml: "1em" }}
                      >
                        {vinyl.vinyl_format}
                      </Typography>

                      {/* Vinyl title */}
                      <Typography
                        gutterBottom
                        variant="subtitle2"
                        component="div"
                        color="white"
                      >
                        {vinyl.vinyl_title}
                      </Typography>
                    </CardContent>
                  </StyledCardActionArea>
                </Collapse>
                <Collapse
                  in={expandedStates[vinyl.vinyl_id]}
                  timeout={300}
                  unmountOnExit
                >
                  <CardContent
                    sx={{
                      padding: 1.3,
                      overflowY: "auto",
                      maxHeight: "300px",
                      "&::-webkit-scrollbar": {
                        width: "6px",
                      },
                      "&::-webkit-scrollbar-thumb": {
                        backgroundColor: "#555",
                        borderRadius: "3px",
                      },
                      "&::-webkit-scrollbar-track": {
                        backgroundColor: "#2a2a2a",
                      },
                    }}
                  >
                    {lstSongs.map(
                      (song, index) =>
                        song.vinyl_id === vinyl.vinyl_id && (
                          <Typography
                            key={index}
                            variant="body2"
                            color="text.secondary"
                            fontSize="0.8em"
                            align="left"
                            sx={{
                              cursor: "pointer",
                              "&:hover": {
                                color: "#b7b7b7",
                              },
                              color:
                                songPlaying &&
                                songPlaying.song_id === song.song_id
                                  ? "#b7b7b7"
                                  : "white",
                            }}
                            onClick={() => playSong(song)}
                          >
                            - {song.song_title}
                          </Typography>
                        ),
                    )}
                  </CardContent>
                </Collapse>
                <CardActions
                  sx={{
                    display: "flex",
                    justifyContent: "space-evenly",
                    flexDirection: "row",
                    flexWrap: "nowrap",
                    alignItems: "center",
                    marginTop: "auto",
                    padding: 0.7,
                  }}
                >
                  <Button
                    size="small"
                    color="primary"
                    href={vinyl.vinyl_link}
                    target="_blank"
                  >
                    <ShoppingCartCheckoutIcon />
                    {/* <Typography */}
                    {/*   variant="caption" */}
                    {/*   sx={{ ml: 0.5, display: { xs: "none", sm: "block" } }} */}
                    {/*   fontSize="0.8em" */}
                    {/* > */}
                    {/*   {vinyl.vinyl_price} {vinyl.vinyl_currency} */}
                    {/* </Typography> */}
                  </Button>
                  {isLoggedIn ? (
                    <Button
                      size="small"
                      color="primary"
                      onClick={() => toggleFavori(vinyl)}
                    >
                      {lstFavoris.some(
                        (favori) => favori.vinyl_id === vinyl.vinyl_id,
                      ) ? (
                        <FavoriteIcon color="secondary" />
                      ) : (
                        <FavoriteBorderIcon color="primary" />
                      )}
                    </Button>
                  ) : null}

                  {/* button play */}
                  <Button
                    size="small"
                    color="primary"
                    onClick={() =>
                      playSong(
                        lstSongs.find(
                          (song) => song.vinyl_id === vinyl.vinyl_id,
                        ),
                      )
                    }
                  >
                    {songPlaying && songPlaying.vinyl_id === vinyl.vinyl_id ? (
                      <PauseIcon color="secondary" />
                    ) : (
                      <PlayArrowIcon color="primary" />
                    )}
                  </Button>

                  <ExpandMore
                    expand={expandedStates[vinyl.vinyl_id]}
                    onClick={() => handleExpandClick(vinyl.vinyl_id)}
                    aria-expanded={expandedStates[vinyl.vinyl_id]}
                    aria-label="show more"
                  >
                    <ExpandMoreIcon />
                  </ExpandMore>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </InfiniteScroll>
    </Box>
  );
}

export default SectionVinyls;

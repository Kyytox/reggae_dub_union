import { useState, useRef } from "react";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Slider from "@mui/material/Slider";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import PauseIcon from "@mui/icons-material/Pause";
import SkipNextIcon from "@mui/icons-material/SkipNext";
import SkipPreviousIcon from "@mui/icons-material/SkipPrevious";
import ShuffleIcon from "@mui/icons-material/Shuffle";
import SectionVinyls from "../components/SectionVinyls";
import "../App.css";

import ReactPlayer from "react-player";

function AudioPlayer({
  lstSongs,
  lstVinyls,
  lstFavoris,
  setLstFavoris,
  loadMoreData,
  topLoadMore,
}) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [songPlaying, setSongPlaying] = useState(null);
  const [isShuffle, setIsShuffle] = useState(false);

  const [progress, setProgress] = useState({ playedSeconds: 0, played: 0 });
  const [duration, setDuration] = useState(0);
  const playerRef = useRef(null);

  // create a function to play the song
  const playSong = (song) => {
    // if the song is already playing, pause it
    if (songPlaying === song) {
      setIsPlaying(false);
      setSongPlaying(null);
    } else {
      // else, play the song
      setIsPlaying(true);
      setSongPlaying(song);
    }
  };

  // function to play the song
  const playShuffleSong = () => {
    // get a random song
    const randomSong = lstSongs[Math.floor(Math.random() * lstSongs.length)];
    setSongPlaying(randomSong);
  };

  //  function to play the next song
  const playNextSong = () => {
    // get the index of the song playing
    const index = lstSongs.findIndex((song) => song === songPlaying);

    // if the shuffle mode is activated, play a random song
    if (isShuffle) {
      playShuffleSong();
    } else {
      // if is the last one, play the first one
      if (index === lstSongs.length - 1) {
        setSongPlaying(lstSongs[0]);
      } else {
        setSongPlaying(lstSongs[index + 1]);
      }
    }
  };

  //  function to play the previous song
  const playPreviousSong = () => {
    // get the index of the song playing
    const index = lstSongs.findIndex((song) => song === songPlaying);

    // if the shuffle mode is activated, play a random song
    if (isShuffle) {
      playShuffleSong();
    } else {
      // if the song playing is the first one, play the last one
      if (index === 0) {
        setSongPlaying(lstSongs[lstSongs.length - 1]);
      } else {
        setSongPlaying(lstSongs[index - 1]);
      }
    }
  };

  // Helper function to format time in MM:SS
  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds < 10 ? "0" : ""}${remainingSeconds}`;
  };

  // Function to handle slider change
  const handleSeek = (e) => {
    const newPlayed = parseFloat(e.target.value);
    playerRef.current.seekTo(newPlayed);
  };

  return (
    <div className="container-audioPlayer">
      <Box
        className="container-audioPlayer-ReactPlayer"
        sx={{
          position: "fixed",
          bottom: 0,
          zIndex: 10,
          width: "100%",
          display: "flex",
          flexDirection: "row",
          flexWrap: "wrap",
          justifyContent: "center",
          alignItems: "center",
          padding: "10px",
          color: "white",
        }}
      >
        <ReactPlayer
          ref={playerRef}
          url={songPlaying ? songPlaying.song_mp3 : null}
          playing={isPlaying}
          volume={1}
          width="0px"
          height="0px"
          onEnded={() => {
            playNextSong();
          }}
          onError={() => {
            playNextSong();
          }}
          progressInterval={1000}
          onProgress={(progress) => setProgress(progress)}
          onDuration={(duration) => setDuration(duration)}
        />
        <Box
          className="container-audioPlayer-controls"
          sx={{
            display: "flex",
            flexDirection: "row",
            alignItems: "end",
            gap: 2,
            marginRight: "20px",
          }}
        >
          <SkipPreviousIcon
            className="container-audioPlayer-player-controls-icon"
            onClick={() => {
              playPreviousSong();
            }}
            cursor="pointer"
          />
          {isPlaying ? (
            <PauseIcon
              className="container-audioPlayer-icon-play"
              onClick={() => {
                setIsPlaying(false);
              }}
              cursor="pointer"
            />
          ) : (
            <PlayArrowIcon
              className="container-audioPlayer-icon-play"
              onClick={() => {
                setIsPlaying(true);
              }}
              cursor="pointer"
            />
          )}
          <SkipNextIcon
            className="container-audioPlayer-player-controls-icon"
            onClick={() => {
              playNextSong();
            }}
            cursor="pointer"
          />
          <ShuffleIcon
            className="container-audioPlayer-player-controls-icon"
            onClick={() => {
              setIsShuffle(!isShuffle);
              playShuffleSong();
            }}
            cursor="pointer"
          />
        </Box>
        <Box
          className="container-audioPlayer-song-info"
          sx={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            paddingLeft: "10px",
            paddingRight: "10px",
            width: "60%",
            color: "white",
          }}
        >
          {songPlaying ? (
            <>
              <Box display="flex" alignItems="center" flexDirection="column">
                <Typography
                  sx={{
                    fontSize: "14px",
                    fontWeight: "bold",
                    textAlign: "center",
                  }}
                >
                  {songPlaying.vinyl_title}
                </Typography>
                <Typography
                  sx={{
                    fontSize: "13px",
                    textAlign: "center",
                  }}
                >
                  {songPlaying.song_title}
                </Typography>
              </Box>
              <Box
                display="flex"
                flexDirection="row"
                alignItems="center"
                width="100%"
              >
                <Typography variant="body2" sx={{ mr: 1 }}>
                  {formatTime(progress.playedSeconds)}
                </Typography>
                <Slider
                  aria-label="time-slider"
                  value={progress.played}
                  min={0}
                  max={1}
                  step={1}
                  onChange={handleSeek}
                  sx={{
                    "& .MuiSlider-thumb": {
                      color: "white",
                    },
                    "& .MuiSlider-rail": {
                      backgroundColor: "#555555",
                    },
                    "& .MuiSlider-thumb": {
                      display: "none", // Hide the thumb
                    },
                  }}
                />
                <Typography variant="body2" sx={{ ml: 1 }}>
                  {formatTime(duration)}
                </Typography>
              </Box>
            </>
          ) : null}
        </Box>
      </Box>

      <div className="container-audioPlayer-lstVinyls">
        <SectionVinyls
          lstVinyls={lstVinyls}
          lstSongs={lstSongs}
          playSong={playSong}
          songPlaying={songPlaying}
          lstFavoris={lstFavoris}
          setLstFavoris={setLstFavoris}
          loadMoreData={loadMoreData}
          topLoadMore={topLoadMore}
        />
      </div>
    </div>
  );
}

export default AudioPlayer;

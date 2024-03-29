import { useState } from "react";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import PauseIcon from "@mui/icons-material/Pause";
import SkipNextIcon from "@mui/icons-material/SkipNext";
import SkipPreviousIcon from "@mui/icons-material/SkipPrevious";
import ShuffleIcon from "@mui/icons-material/Shuffle";
import LstVinyls from "./LstVinyls";
import "../App.css";

import ReactPlayer from "react-player";

function AudioPlayer({ lstSongs, lstFavoris, setLstFavoris, loadMoreData }) {
    const [isPlaying, setIsPlaying] = useState(false);
    const [songPlaying, setSongPlaying] = useState(null);
    const [isShuffle, setIsShuffle] = useState(false);

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

    // create a function to play the song
    const playShuffleSong = () => {
        // get a random song
        const randomSong =
            lstSongs[Math.floor(Math.random() * lstSongs.length)];
        setSongPlaying(randomSong);
    };

    // create a function to play the next song
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

    // create a function to play the previous song
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

    return (
        <div className="container-audioPlayer">
            <div className="container-audioPlayer-ReactPlayer bg-zinc-800 fixed bottom-0 z-10 p-2 w-full flex justify-start items-center">
                <ReactPlayer
                    url={songPlaying ? songPlaying.song_mp3 : null}
                    playing={isPlaying}
                    volume={0.5}
                    width="0px"
                    height="0px"
                    onEnded={() => {
                        playNextSong();
                    }}
                    onError={() => {
                        playNextSong();
                    }}
                    progressInterval={1000}
                />
                <div className="container-audioPlayer-controls mr-6">
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
                    <SkipPreviousIcon
                        className="container-audioPlayer-player-controls-icon"
                        onClick={() => {
                            playPreviousSong();
                        }}
                        cursor="pointer"
                    />
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
                </div>
                <div className="container-audioPlayer-title">
                    {songPlaying ? songPlaying.title : null}-
                    {songPlaying ? songPlaying.song_title : null}
                </div>
            </div>
            <div className="container-audioPlayer-lstVinyls mt-6">
                <LstVinyls
                    lstVinyls={lstSongs}
                    playSong={playSong}
                    songPlaying={songPlaying}
                    lstFavoris={lstFavoris}
                    setLstFavoris={setLstFavoris}
                    loadMoreData={loadMoreData}
                />
            </div>
        </div>
    );
}

export default AudioPlayer;

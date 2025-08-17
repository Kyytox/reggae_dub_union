import { useContext, useEffect, useState } from "react";
import { AuthContext } from "./AuthContext";
import { useNavigate } from "react-router-dom";
import { getAxiosAuth } from "./UtilsAxios";
import AudioPlayer from "./AudioPlayer";
import LstShops from "./LstShops";
import LstFormatVinyls from "./LstFormatVinyls";
import "../App.css";

function Favoris() {
  const navigate = useNavigate();
  const nbVinyls = 100; // number of vinyls to display
  const { isLoggedIn, idUser, logout } = useContext(AuthContext);
  const [lstVinyls, setLstVinyls] = useState([]);
  const [lstVinylsSelected, setLstVinylsSelected] = useState([]);
  const [lstSongs, setLstSongs] = useState([]);
  const [lstSongsSelected, setLstSongsSelected] = useState([]);
  const [lstShops, setLstShops] = useState([]);
  const [lstShopsSelected, setLstShopsSelected] = useState([]);
  const [lstFormatVinyls, setLstFormatVinyls] = useState([]);
  const [lstFormatVinylsSelected, setLstFormatVinylsSelected] = useState([]);
  const [lstFavoris, setLstFavoris] = useState([]);

  const FetchData = async () => {
    try {
      // get data
      console.log("isLoggedIn", isLoggedIn, idUser);
      if (isLoggedIn) {
        const vinylsSongs = await getAxiosAuth("/get_favoris", idUser);
        if (vinylsSongs === "Token is not valid") {
          logout();
          navigate("/login");
        }

        console.log("vinylsSongs", vinylsSongs);

        if (typeof vinylsSongs === "string") {
          console.log("Error fetching data:", vinylsSongs);
        } else {
          // get Vinyls, Songs, Shops
          const vinyls = vinylsSongs["vinyls"];
          const songs = vinylsSongs["songs"];
          const shops = vinylsSongs["shops"];
          const favoris = vinylsSongs["favoris"];

          // update States
          setLstShops(shops);
          getUniqueFormatVinyls(vinyls);
          setLstVinyls(vinyls);
          setLstSongs(songs);
          setLstFavoris(favoris);
          setLstSongsSelected(songs.slice(0, nbVinyls)); // get first x songs
          setLstVinylsSelected(vinyls.slice(0, nbVinyls)); // get first x vinyls
        }
      } else {
        navigate("/login");
      }
    } catch (error) {
      console.error("Une erreur s'est produite :", error);
    }
  };

  // get Vinyls and Songs
  useEffect(() => {
    FetchData();
  }, []);

  useEffect(() => {
    // get all vinyls from selected shops, if no shop is selected, get all vinyls
    const newLstVinyls =
      lstShopsSelected.length === 0
        ? lstVinyls
        : lstVinyls.filter((vinyl) => lstShopsSelected.includes(vinyl.shop_id));

    // filter by selected format vinyls, if any
    const filteredLstVinyls =
      lstFormatVinylsSelected.length === 0
        ? newLstVinyls
        : newLstVinyls.filter((vinyl) =>
            lstFormatVinylsSelected.includes(vinyl.vinyl_format),
          );

    // with vinyl_id, get songs
    const newLstSongs = filteredLstVinyls.map((vinyl) => {
      return lstSongs.filter((song) => song.vinyl_id === vinyl.vinyl_id);
    });

    setLstVinylsSelected(filteredLstVinyls.slice(0, nbVinyls));
    setLstSongsSelected(newLstSongs.slice(0, nbVinyls));

    getUniqueFormatVinyls(newLstVinyls);
  }, [lstShopsSelected, lstFormatVinylsSelected]);

  const getUniqueFormatVinyls = (lstVinyls) => {
    const lstFormatVinyls = lstVinyls
      .map((vinyl) => vinyl.vinyl_format)
      .filter((value, index, self) => self.indexOf(value) === index);
    setLstFormatVinyls(lstFormatVinyls);
  };

  if (lstVinylsSelected.length === 0) {
    return (
      <div className="favoris">
        <h2>You have no favorites yet!</h2>
      </div>
    );
  }
  return (
    <div className="favoris">
      <LstShops
        lstShops={lstShops}
        lstShopsSelected={lstShopsSelected}
        setLstShopsSelected={setLstShopsSelected}
      />
      <LstFormatVinyls
        lstFormatVinyls={lstFormatVinyls}
        lstFormatVinylsSelected={lstFormatVinylsSelected}
        setLstFormatVinylsSelected={setLstFormatVinylsSelected}
      />
      <AudioPlayer
        lstSongs={lstSongsSelected}
        lstVinyls={lstVinylsSelected}
        lstFavoris={lstFavoris}
        setLstFavoris={setLstFavoris}
      />
    </div>
  );
}

export default Favoris;

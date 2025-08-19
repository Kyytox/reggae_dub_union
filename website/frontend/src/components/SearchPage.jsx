import { useContext, useEffect, useState } from "react";
import { AuthContext } from "./AuthContext";
import { getAxios, getAxiosAuth } from "./UtilsAxios";
import { useParams } from "react-router-dom";
import AudioPlayer from "./AudioPlayer";
import LstShops from "./LstShops";
import LstFormatVinyls from "./LstFormatVinyls";
import "../App.css";

// composant for Search not found
function SearchNotFound() {
  return (
    <div className="noResult" style={{ marginTop: "5em" }}>
      <h2>No result found</h2>
    </div>
  );
}

function SearchPage() {
  const { search } = useParams();

  const { isLoggedIn, idUser } = useContext(AuthContext);
  const nbVinyls = 100;
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
      const search_response = await getAxios("/search/" + search);
      console.log("search_response", search_response);

      // if result contans error key
      if (search_response.error) {
        return <SearchNotFound />;
      }

      // if result contans message key
      if (search_response.error) {
        return <SearchNotFound />;
      }

      // get Vinyls, Songs, Shops
      const vinyls = search_response["vinyls"];
      const songs = search_response["songs"];
      const shops = search_response["shops"];

      // if user is connect get favoris
      if (isLoggedIn) {
        const favoris = await getAxiosAuth("/get_list_favoris", idUser);
        if (favoris === "Token is not valid") {
          logout();
          navigate("/login");
        }
        console.log("favoris", favoris);
        setLstFavoris(favoris);
      }

      // update States
      setLstShops(shops);
      getUniqueFormatVinyls(vinyls);
      setLstVinyls(vinyls);
      setLstSongs(songs);
      setLstSongsSelected(songs.slice(0, nbVinyls)); // get first x songs
      setLstVinylsSelected(vinyls.slice(0, nbVinyls)); // get first x vinyls
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

  return (
    <div className="home">
      <>
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
          // loadMoreData={loadMoreData}
        />
      </>
    </div>
  );
}

export default SearchPage;

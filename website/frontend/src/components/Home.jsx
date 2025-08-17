import { useContext, useEffect, useState } from "react";
import { AuthContext } from "./AuthContext";
import { getAxios, getAxiosAuth } from "./UtilsAxios";
import AudioPlayer from "./AudioPlayer";
import LstShops from "./LstShops";
import LstFormatVinyls from "./LstFormatVinyls";
import "../App.css";

function Home() {
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
      const vinylsSongs = await getAxios("/get_vinyls_songs");
      console.log("vinylsSongs", vinylsSongs);

      // get Vinyls, Songs, Shops
      const vinyls = vinylsSongs["vinyls"];
      const songs = vinylsSongs["songs"];
      const shops = vinylsSongs["shops"];

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

  const loadMoreData = () => {
    // collect last id of lstVinylsSelected
    const lastId = lstVinylsSelected[lstVinylsSelected.length - 1].vinyl_id;

    // get 200 vinyls after lastId (inferior to lastId)
    const newLstVinyls = lstVinyls
      .filter((vinyl) => vinyl.vinyl_id < lastId)
      .slice(0, nbVinyls);

    // append newLstVinyls to lstVinylsSelected
    setLstVinylsSelected([...lstVinylsSelected, ...newLstVinyls]);
  };
  console.log("slt favoris ", lstFavoris);

  return (
    <div className="home">
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
        loadMoreData={loadMoreData}
      />
    </div>
  );
}

export default Home;

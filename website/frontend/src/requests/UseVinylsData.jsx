import { useContext, useEffect, useState } from "react";
import { AuthContext } from "../components/AuthContext";
import { useNavigate } from "react-router-dom";
import { getAxiosAuth, getAxios } from "../requests/UtilsAxios";

import ResultEmpty from "../errors/ResultEmpty";
import PageNotFound from "../errors/PageNotFound";

import "../App.css";

const nbVinyls = 100;

function useVinylsData(apiEndpoint) {
  const navigate = useNavigate();
  const { isLoggedIn, idUser, logout } = useContext(AuthContext);
  const [topLoadMore, setTopLoadMore] = useState(true);
  const [totalVinyls, setTotalVinyls] = useState(0);
  const [numPage, setNumPage] = useState(1);
  const [nbPages, setNbPages] = useState(1);

  const [lstVinyls, setLstVinyls] = useState([]);
  const [lstVinylsSelected, setLstVinylsSelected] = useState([]);

  const [lstSongs, setLstSongs] = useState([]);
  const [lstSongsSelected, setLstSongsSelected] = useState([]);

  const [lstShops, setLstShops] = useState([]);
  const [lstShopsSelected, setLstShopsSelected] = useState([]);

  const [lstFormatVinyls, setLstFormatVinyls] = useState([]);
  const [lstFormatVinylsSelected, setLstFormatVinylsSelected] = useState([]);

  const [lstFavoris, setLstFavoris] = useState([]);

  const getPresentFormatVinyls = (vinyls) => {
    // get formats in vinyls and update lstFormatVinylsSelected
    const formats = [...new Set(vinyls.map((vinyl) => vinyl.vinyl_format))];
    setLstFormatVinylsSelected(formats);
  };

  const fetchInitialData = async () => {
    try {
      // get all shops
      const allShops = await getAxios("/get_all_shops");
      setLstShops(allShops);

      // get all formats
      const allFormats = await getAxios("/get_all_formats");
      setLstFormatVinyls(allFormats);

      // get nb vinyls
      const data_nb_vinyls = await getAxios("/get_nb_vinyls");
      const nbVinylsTotal = data_nb_vinyls.nb_vinyls || 0;

      setNbPages(Math.ceil(nbVinylsTotal / (nbVinyls * 3)));
    } catch (error) {
      console.error("An error occurred:", error);
    }
  };

  const fetchData = async () => {
    try {
      let vinylsSongs;
      console.log("shop selected", lstShopsSelected);
      console.log("format selected", lstFormatVinylsSelected);

      if (apiEndpoint === "home") {
        // prepare data
        console.log("fetch page numPage", numPage);
        const data_filters = {
          shops: lstShopsSelected,
          formats: lstFormatVinylsSelected,
          num_page: numPage,
        };
        vinylsSongs = await getAxios("/get_vinyls_songs", data_filters);
      } else if (apiEndpoint.includes("search")) {
        // get search
        const search = apiEndpoint.split("/").pop();

        // get search results
        vinylsSongs = await getAxios("/search/" + search);
        console.log("vinylsSongs", vinylsSongs);

        if (vinylsSongs.error) {
          console.error("No results found for search:", search);
          return <ResultEmpty />;
        }
      } else if (apiEndpoint === "favoris") {
        if (!isLoggedIn) {
          navigate("/login");
        }

        // get favoris from user
        vinylsSongs = await getAxiosAuth("/get_favoris", idUser);
        const favoris = vinylsSongs.favoris || [];
        setLstFavoris(favoris);

        if (vinylsSongs.error) {
          logout();
          navigate("/login");
        }
      } else {
        console.error("Page not found");
        return <PageNotFound />;
      }

      // get favoris if endpoint is not favoris
      if (isLoggedIn && apiEndpoint !== "favoris") {
        const favoris = await getAxiosAuth("/get_list_favoris", idUser);

        if (favoris.error) {
          logout();
          navigate("/login");
        }
        setLstFavoris(favoris);
      }

      const vinyls = vinylsSongs.vinyls || [];
      const songs = vinylsSongs.songs || [];
      const shops = vinylsSongs.shops || [];

      // setLstShops(shops);
      getPresentFormatVinyls(vinyls);
      setLstVinyls(vinyls);
      setLstSongs(songs);

      // Initialize Vinyls
      const firstVinyls = vinyls.slice(0, nbVinyls);
      setLstVinylsSelected(firstVinyls);
      setTotalVinyls(vinyls.length);

      // Initialize lstSongsSelected based on the first nbVinyls vinyls
      const initialSongs = firstVinyls.flatMap((vinyl) =>
        songs.filter((song) => song.vinyl_id === vinyl.vinyl_id),
      );
      setLstSongsSelected(initialSongs);

      // Check if all vinyls are selected
      if (parseInt(vinyls.length, 10) <= nbVinyls) {
        setTopLoadMore(false);
      }
    } catch (error) {
      console.error("An error occurred:", error);
    }
  };

  useEffect(() => {
    fetchInitialData();
    fetchData();
  }, [apiEndpoint, isLoggedIn]); // Re-fetch data when endpoint or login status changes

  const clickChangePage = (num) => {
    console.log("clickFetchData called");
    setNumPage(num);
    fetchData();
  };

  // Filtering logic
  // useEffect(() => {
  //   let newLstVinyls =
  //     lstShopsSelected.length === 0
  //       ? lstVinyls
  //       : lstVinyls.filter((vinyl) => lstShopsSelected.includes(vinyl.shop_id));
  //
  //   const filteredLstVinyls =
  //     lstFormatVinylsSelected.length === 0
  //       ? newLstVinyls
  //       : newLstVinyls.filter((vinyl) =>
  //           lstFormatVinylsSelected.includes(vinyl.vinyl_format),
  //         );
  //
  //   setLstVinylsSelected(filteredLstVinyls.slice(0, nbVinyls));
  //
  //   // get songs for the first nbVinyls vinyls
  //   const initialSongs = filteredLstVinyls
  //     .slice(0, nbVinyls)
  //     .flatMap((vinyl) =>
  //       lstSongs.filter((song) => song.vinyl_id === vinyl.vinyl_id),
  //     );
  //   setLstSongsSelected(initialSongs);
  // }, [lstShopsSelected, lstFormatVinylsSelected]);

  const loadMoreData = () => {
    console.log("loadMoreData called");
    if (lstVinylsSelected.length === 0) return;

    // Load more vinyls based on the last selected vinyl
    // const lastId = lstVinylsSelected[lstVinylsSelected.length - 1].vinyl_id;
    const lastId = lstVinylsSelected[lstVinylsSelected.length - 1].id_elem;
    const newVinyls = lstVinyls
      .filter((vinyl) => vinyl.id_elem > lastId)
      .slice(0, nbVinyls);
    setLstVinylsSelected([...lstVinylsSelected, ...newVinyls]);

    // Update lstSongsSelected
    const newSongs = newVinyls.flatMap((vinyl) =>
      lstSongs.filter((song) => song.vinyl_id === vinyl.vinyl_id),
    );
    setLstSongsSelected([...lstSongsSelected, ...newSongs]);

    // check if all vinyls are selected
    if (
      parseInt(lstVinylsSelected.length, 10) === parseInt(lstVinyls.length, 10)
    ) {
      setTopLoadMore(false);
    } else {
      setTopLoadMore(true);
    }
  };

  return {
    fetchData,
    lstVinylsSelected,
    lstSongsSelected,
    lstShops,
    lstShopsSelected,
    setLstShopsSelected,
    lstFormatVinyls,
    lstFormatVinylsSelected,
    setLstFormatVinylsSelected,
    lstFavoris,
    setLstFavoris,
    loadMoreData,
    topLoadMore,
    clickChangePage: clickChangePage,
    nbPages,
  };
}

export default useVinylsData;

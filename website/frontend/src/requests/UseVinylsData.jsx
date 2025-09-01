import { useContext, useEffect, useState } from "react";
import { AuthContext } from "../components/AuthContext";
import { useNavigate } from "react-router-dom";
import { getAxiosAuth, getAxios } from "../requests/UtilsAxios";

import ResultEmpty from "../errors/ResultEmpty";
import PageNotFound from "../errors/PageNotFound";

import "../App.css";

const nbVinyls = 100;

function useVinylsData(
  apiEndpoint,
  lstShopsSelected = [],
  lstFormatsSelected = [],
) {
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

  const [lstFavoris, setLstFavoris] = useState([]);

  // Prepare data filters
  const prepareDataFilters = (
    shops = null,
    formats = null,
    random = false,
    searchVal = null,
  ) => {
    return {
      shops: shops || lstShopsSelected,
      formats: formats || lstFormatsSelected,
      search: searchVal,
      num_page: numPage,
      top_random: random,
    };
  };

  const initNumPages = async () => {
    setNumPage(1);
  };

  const fetchData = async () => {
    try {
      let vinylsSongs;
      let nbVinylsTotal = 0;
      const endpointValue = apiEndpoint.split("/").pop();

      if (apiEndpoint === "home") {
        //
        // prepare data
        const data_filters = prepareDataFilters();
        const data_nb_vinyls = await getAxios("/get_nb_vinyls", data_filters);
        nbVinylsTotal = data_nb_vinyls.nb_vinyls;
        vinylsSongs = await getAxios("/get_vinyls_songs", data_filters);
      } else if (apiEndpoint.includes("search")) {
        //
        // get search results
        const data_filters = prepareDataFilters(
          null,
          null,
          false,
          endpointValue,
        );
        console.log("data_filters", data_filters);
        const data_nb_vinyls = await getAxios("/get_nb_vinyls", data_filters);
        nbVinylsTotal = data_nb_vinyls.nb_vinyls;
        vinylsSongs = await getAxios("/search/" + endpointValue);
      } else if (apiEndpoint === "favoris") {
        if (!isLoggedIn) {
          navigate("/login");
        }

        // get favoris from user
        const data_nb_vinyls = await getAxios("/get_nb_vinyls", data_filters);
        nbVinylsTotal = data_nb_vinyls.nb_vinyls;
        vinylsSongs = await getAxiosAuth("/get_favoris", idUser);
        const favoris = vinylsSongs.favoris || [];
        setLstFavoris(favoris);

        if (vinylsSongs.error) {
          logout();
          navigate("/login");
        }
      } else if (apiEndpoint.includes("uniqueShop")) {
        //
        // prepare data
        const data_filters = prepareDataFilters(
          [endpointValue],
          null,
          false,
          null,
        );
        const data_nb_vinyls = await getAxios("/get_nb_vinyls", data_filters);
        nbVinylsTotal = data_nb_vinyls.nb_vinyls;
        vinylsSongs = await getAxios("/get_vinyls_songs", data_filters);
      } else if (apiEndpoint.includes("uniqueFormat")) {
        //
        // prepare data
        const data_filters = prepareDataFilters(
          null,
          [endpointValue],
          false,
          null,
        );
        const data_nb_vinyls = await getAxios("/get_nb_vinyls", data_filters);
        nbVinylsTotal = data_nb_vinyls.nb_vinyls;
        vinylsSongs = await getAxios("/get_vinyls_songs", data_filters);
      } else if (apiEndpoint === "random") {
        //
        // prepare data
        const data_filters = prepareDataFilters(null, null, true, null);
        const data_nb_vinyls = await getAxios("/get_nb_vinyls", data_filters);
        nbVinylsTotal = data_nb_vinyls.nb_vinyls;
        vinylsSongs = await getAxios("/get_vinyls_songs", data_filters);
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

      setTotalVinyls(nbVinylsTotal);
      setLstVinyls(vinyls);
      setLstSongs(songs);

      // Initialize Vinyls
      const firstVinyls = vinyls.slice(0, nbVinyls);
      setLstVinylsSelected(firstVinyls);

      // Initialize lstSongsSelected based on the first nbVinyls vinyls
      const initialSongs = firstVinyls.flatMap((vinyl) =>
        songs.filter((song) => song.vinyl_id === vinyl.vinyl_id),
      );
      setLstSongsSelected(initialSongs);

      // Calculate number of pages
      setNbPages(Math.ceil(nbVinylsTotal / vinyls.length));

      // Check if all vinyls are selected
      if (parseInt(vinyls.length, 10) <= nbVinyls) {
        setTopLoadMore(false);
      }
    } catch (error) {
      console.error("An error occurred:", error);
    }
  };

  useEffect(() => {
    initNumPages();
  }, [apiEndpoint]);

  useEffect(() => {
    fetchData();
    window.scrollTo(0, 0); // put user in top of the page
  }, [apiEndpoint, isLoggedIn, numPage]); // Re-fetch data when endpoint or login status changes

  const clickChangePage = (num) => {
    setNumPage(num);
  };

  const clickApplyFilters = () => {
    initNumPages();
    fetchData();
  };

  const loadMoreData = () => {
    if (lstVinylsSelected.length === 0) return;

    // Load more vinyls based on the last selected vinyl
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
    lstVinylsSelected,
    lstSongsSelected,
    lstFavoris,
    setLstFavoris,
    loadMoreData,
    topLoadMore,
    clickChangePage: clickChangePage,
    clickApplyFilters: clickApplyFilters,
    nbPages,
    totalVinyls,
  };
}

export default useVinylsData;

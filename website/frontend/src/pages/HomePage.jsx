import { useContext, useEffect, useState } from "react";
import AudioPlayer from "../components/AudioPlayer";
import Box from "@mui/material/Box";
import SectionFilter from "../components/SectionFilter";
import useVinylsData from "../requests/UseVinylsData";
import SectionPagination from "../components/SectionPagination";

import { getAxios } from "../requests/UtilsAxios";

import "../App.css";

function Home() {
  // State for shops and formats
  const [lstShops, setLstShops] = useState([]);
  const [lstShopsSelected, setLstShopsSelected] = useState([]);
  const [lstFormats, setLstFormats] = useState([]);
  const [lstFormatsSelected, setLstFormatsSelected] = useState([]);

  const fetchDataHome = async () => {
    try {
      // get all shops
      if (lstShops.length === 0) {
        const allShops = await getAxios("/get_all_shops");
        setLstShops(allShops);
        // setLstShopsSelected(allShops.map((shop) => shop));
      }

      // get all formats
      if (lstFormats.length === 0) {
        const allFormats = await getAxios("/get_all_formats");
        setLstFormats(allFormats);
        // setLstFormatsSelected(allFormats.map((format) => format));
      }
    } catch (error) {
      console.error("An error occurred:", error);
    }
  };

  useEffect(() => {
    console.log("UseEffect Home");
    fetchDataHome();
  }, []);

  const {
    lstVinylsSelected,
    lstSongsSelected,
    lstFavoris,
    setLstFavoris,
    loadMoreData,
    topLoadMore,
    clickChangePage,
    clickApplyFilters,
    nbPages,
  } = useVinylsData("home", lstShopsSelected, lstFormatsSelected);

  return (
    <Box className="main-content">
      <Box>
        <h1>All Vinyls</h1>
      </Box>

      <Box className="main-content-container">
        <SectionFilter
          clickApplyFilters={clickApplyFilters}
          lstShops={lstShops}
          lstShopsSelected={lstShopsSelected}
          setLstShopsSelected={setLstShopsSelected}
          lstFormats={lstFormats}
          lstFormatsSelected={lstFormatsSelected}
          setLstFormatsSelected={setLstFormatsSelected}
        />
        <AudioPlayer
          lstSongs={lstSongsSelected}
          lstVinyls={lstVinylsSelected}
          lstFavoris={lstFavoris}
          setLstFavoris={setLstFavoris}
          loadMoreData={loadMoreData}
          topLoadMore={topLoadMore}
        />
      </Box>
      <SectionPagination nbPages={nbPages} clickChangePage={clickChangePage} />
    </Box>
  );
}

export default Home;

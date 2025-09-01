import { useContext, useEffect, useState } from "react";
import AudioPlayer from "../components/AudioPlayer";
import Box from "@mui/material/Box";
import SectionFilter from "../components/SectionFilter";
import useVinylsData from "../requests/UseVinylsData";
import HeadPage from "../components/HeadPage";
import SectionPagination from "../components/SectionPagination";
import ResultEmpty from "../errors/ResultEmpty";

import { getAxios } from "../requests/UtilsAxios";

import "../App.css";

function RandomPage() {
  // State for shops and formats
  const [lstShops, setLstShops] = useState([]);
  const [lstShopsSelected, setLstShopsSelected] = useState([]);
  const [lstFormats, setLstFormats] = useState([]);
  const [lstFormatsSelected, setLstFormatsSelected] = useState([]);

  const fetchDataRandom = async () => {
    try {
      // get all shops
      if (lstShops.length === 0) {
        const allShops = await getAxios("/get_all_shops");
        setLstShops(allShops);
      }

      // get all formats
      if (lstFormats.length === 0) {
        const allFormats = await getAxios("/get_all_formats");
        setLstFormats(allFormats);
      }
    } catch (error) {
      console.error("An error occurred:", error);
    }
  };

  useEffect(() => {
    console.log("UseEffect RandomPage");
    fetchDataRandom();
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
    totalVinyls,
  } = useVinylsData("random", lstShopsSelected, lstFormatsSelected);

  return (
    <>
      {lstVinylsSelected.length === 1 ? (
        <ResultEmpty />
      ) : (
        <Box className="main-content">
          <SectionFilter
            clickApplyFilters={clickApplyFilters}
            lstShops={lstShops}
            lstShopsSelected={lstShopsSelected}
            setLstShopsSelected={setLstShopsSelected}
            lstFormats={lstFormats}
            lstFormatsSelected={lstFormatsSelected}
            setLstFormatsSelected={setLstFormatsSelected}
          />
          <Box className="main-content-container">
            <HeadPage
              text={`Random Vinyls`}
              totalVinyls={lstVinylsSelected.length}
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
          {/*<SectionPagination nbPages={nbPages} clickChangePage={clickChangePage} />*/}
        </Box>
      )}
    </>
  );
}

export default RandomPage;

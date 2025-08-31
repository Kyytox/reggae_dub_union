import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import AudioPlayer from "../components/AudioPlayer";
import Box from "@mui/material/Box";
import SectionFilter from "../components/SectionFilter";
import useVinylsData from "../requests/UseVinylsData";
import { getAxios } from "../requests/UtilsAxios";
import SectionPagination from "../components/SectionPagination";

import "../App.css";

function UniqueFormatPage() {
  const { formatName } = useParams();

  // State for shops and formats
  const [lstShops, setLstShops] = useState([]);
  const [lstShopsSelected, setLstShopsSelected] = useState([]);
  const [lstFormats, setLstFormats] = useState([formatName]);
  const [lstFormatsSelected, setLstFormatsSelected] = useState([formatName]);

  const fetchDataUniqueFormat = async (formatName) => {
    try {
      // Fetch shop details
      const shopDetails = await getAxios(`/get_shops_by_format/${formatName}`);
      //
      setLstShops(shopDetails);
      setLstShopsSelected(shopDetails.map((shop) => shop));
    } catch (error) {
      console.error("Error fetching shop data:", error);
      setLstShops([]);
      setLstFormats([]);
      setLstShopsSelected([]);
      setLstFormatsSelected([]);
    }
  };

  useEffect(() => {
    console.log("UseEffect Unique Format Page");
    if (formatName) {
      fetchDataUniqueFormat(formatName);
    }
  }, [formatName]);

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
  } = useVinylsData("uniqueFormat/" + formatName);

  return (
    <Box className="main-content">
      <Box>
        <h1>Vinyls in {formatName}"</h1>
      </Box>

      <Box className="main-content-container">
        <SectionFilter
          clickApplyFilters={clickApplyFilters}
          lstShops={lstShops}
          lstShopsSelected={lstShopsSelected}
          setLstShopsSelected={setLstShopsSelected}
          lstFormats={null}
          lstFormatsSelected={null}
          setLstFormatsSelected={null}
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

export default UniqueFormatPage;

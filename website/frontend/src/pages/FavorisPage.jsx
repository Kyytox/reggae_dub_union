import { useEffect, useState } from "react";
import AudioPlayer from "../components/AudioPlayer";
import SectionFilter from "../components/SectionFilter";
import useVinylsData from "../requests/UseVinylsData";
import Box from "@mui/material/Box";
import SectionPagination from "../components/SectionPagination";
import HeadPage from "../components/HeadPage";

import ResultEmpty from "../errors/ResultEmpty";

import "../App.css";

function FavorisPage() {
  // State for shops and formats
  const [lstShops, setLstShops] = useState([]);
  const [lstShopsSelected, setLstShopsSelected] = useState([]);
  const [lstFormats, setLstFormats] = useState([]);
  const [lstFormatsSelected, setLstFormatsSelected] = useState([]);

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
  } = useVinylsData("favoris", lstShopsSelected, lstFormatsSelected);

  const fetchDataFavoris = async () => {
    try {
      // get shopw from lstVinylsSelected
      if (lstVinylsSelected.length > 0) {
        const shopsMap = new Map();
        lstVinylsSelected.forEach((vinyl) => {
          shopsMap.set(vinyl.shop_id, {
            shop_id: vinyl.shop_id,
            shop_name: vinyl.shop_name,
          });
        });
        const shopsArray = Array.from(shopsMap.values());
        setLstShops(shopsArray);

        // get all formats from lstVinylsSelected
        const formatsSet = new Set(
          lstVinylsSelected.map((vinyl) => vinyl.vinyl_format),
        );
        const formatsArray = Array.from(formatsSet);
        setLstFormats(formatsArray);
      }
    } catch (error) {
      console.error("An error occurred:", error);
    }
  };

  useEffect(() => {
    console.log("UseEffect FavorisPage");
    fetchDataFavoris();
  }, [lstVinylsSelected]);

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
              text={`Search results for "${search}"`}
              totalVinyls={totalVinyls}
            />
            <SectionPagination
              nbPages={nbPages}
              clickChangePage={clickChangePage}
            />
          </Box>

          <AudioPlayer
            lstSongs={lstSongsSelected}
            lstVinyls={lstVinylsSelected}
            lstFavoris={lstFavoris}
            setLstFavoris={setLstFavoris}
            loadMoreData={loadMoreData}
            topLoadMore={topLoadMore}
          />
        </Box>
      )}
    </>
  );
}
export default FavorisPage;

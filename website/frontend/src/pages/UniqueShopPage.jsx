import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import AudioPlayer from "../components/AudioPlayer";
import Box from "@mui/material/Box";
import SectionFilter from "../components/SectionFilter";
import useVinylsData from "../requests/UseVinylsData";
import { getAxios } from "../requests/UtilsAxios";
import SectionPagination from "../components/SectionPagination";

import "../App.css";

function UniqueShopPage() {
  console.log("Render Unique Format Page");
  const { id_shop } = useParams();

  // State for shops and formats
  const [lstShops, setLstShops] = useState([]);
  const [lstShopsSelected, setLstShopsSelected] = useState([]);
  const [lstFormats, setLstFormats] = useState([]);
  const [lstFormatsSelected, setLstFormatsSelected] = useState([]);

  const fetchDataUniqueShop = async (shopId) => {
    try {
      // Fetch shop details
      const shopDetails = await getAxios(`/get_shop_by_id/${shopId}`);
      setLstShops([shopDetails]);
      setLstShopsSelected([shopDetails.shop_name]);

      // Fetch formats for the specific shop
      const formats = await getAxios(`/get_formats_by_shop/${shopId}`);
      setLstFormats(formats);
      setLstFormatsSelected(formats.map((format) => format));
    } catch (error) {
      console.error("Error fetching shop data:", error);
      setLstShops([]);
      setLstFormats([]);
      setLstShopsSelected([]);
      setLstFormatsSelected([]);
    }
  };

  useEffect(() => {
    console.log("UseEffect Unique Shop Page");
    if (id_shop) {
      fetchDataUniqueShop(id_shop);
    }
  }, [id_shop]);

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
  } = useVinylsData(
    "uniqueShop/" + id_shop,
    lstShopsSelected,
    lstFormatsSelected,
  );

  return (
    <Box className="main-content">
      <Box>
        <h1>Vinyls of the shop {lstShopsSelected}</h1>
      </Box>

      <Box className="main-content-container">
        <SectionFilter
          clickApplyFilters={clickApplyFilters}
          lstShops={null}
          lstShopsSelected={null}
          setLstShopsSelected={null}
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

export default UniqueShopPage;

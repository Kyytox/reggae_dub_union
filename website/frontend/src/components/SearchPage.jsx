import { useParams } from "react-router-dom";
import AudioPlayer from "./AudioPlayer";
import LstShops from "./LstShops";
import LstFormatVinyls from "./LstFormatVinyls";
import useVinylsData from "./UseVinylsData";

import ResultEmpty from "./errors/ResultEmpty";

import "../App.css";

function SearchPage() {
  const { search } = useParams();
  const {
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
    loadMoreData, // loadMoreData is not used in SearchPage
    topLoadMore, // topLoadMore is not used in SearchPage
  } = useVinylsData(`search/${search}`);

  if (lstVinylsSelected.length === 0) {
    return <ResultEmpty />;
  }

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
        topLoadMore={topLoadMore}
      />
    </div>
  );
}

export default SearchPage;

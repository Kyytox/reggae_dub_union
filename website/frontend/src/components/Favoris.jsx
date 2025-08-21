import AudioPlayer from "./AudioPlayer";
import LstShops from "./LstShops";
import LstFormatVinyls from "./LstFormatVinyls";
import useVinylsData from "./UseVinylsData";

import ResultEmpty from "./errors/ResultEmpty";

import "../App.css";

function Favoris() {
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
    loadMoreData,
    topLoadMore,
  } = useVinylsData("favoris");

  if (lstVinylsSelected.length === 0) {
    return <ResultEmpty />;
  }

  return (
    <div className="favoris">
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

export default Favoris;

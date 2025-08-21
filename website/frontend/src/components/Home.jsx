import AudioPlayer from "./AudioPlayer";
import LstShops from "./LstShops";
import LstFormatVinyls from "./LstFormatVinyls";
import useVinylsData from "./UseVinylsData";

import "../App.css";

function Home() {
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
  } = useVinylsData("home");

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

export default Home;

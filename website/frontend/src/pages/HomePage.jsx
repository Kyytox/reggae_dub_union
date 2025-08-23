import AudioPlayer from "../components/AudioPlayer";
import SectionFilter from "../components/SectionFilter";
import useVinylsData from "../requests/UseVinylsData";

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
    <div className="main-content">
      <SectionFilter
        lstItems={lstShops}
        lstItemsSelected={lstShopsSelected}
        setLstItemsSelected={setLstShopsSelected}
        sectionName={"Shops"}
      />
      <SectionFilter
        lstItems={lstFormatVinyls}
        lstItemsSelected={lstFormatVinylsSelected}
        setLstItemsSelected={setLstFormatVinylsSelected}
        sectionName={"Formats"}
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

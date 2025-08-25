import AudioPlayer from "../components/AudioPlayer";
import SectionFilter from "../components/SectionFilter";
import useVinylsData from "../requests/UseVinylsData";
import SectionPagination from "../components/SectionPagination";

import "../App.css";

function Home() {
  const {
    fetchData,
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
    clickChangePage,
    nbPages,
  } = useVinylsData("home");
  // <SectionFilter
  //   lstItems={lstShops}
  //   lstItemsSelected={lstShopsSelected}
  //   setLstItemsSelected={setLstShopsSelected}
  //   sectionName={"Shops"}
  // />
  // <SectionFilter
  //   lstItems={lstFormatVinyls}
  //   lstItemsSelected={lstFormatVinylsSelected}
  //   setLstItemsSelected={setLstFormatVinylsSelected}
  //   sectionName={"Formats"}
  // />

  console.log(nbPages);
  return (
    <div className="main-content">
      <SectionFilter
        fetchData={fetchData}
        lstShops={lstShops}
        lstShopsSelected={lstShopsSelected}
        setLstShopsSelected={setLstShopsSelected}
        lstFormatVinyls={lstFormatVinyls}
        lstFormatVinylsSelected={lstFormatVinylsSelected}
        setLstFormatVinylsSelected={setLstFormatVinylsSelected}
      />
      <SectionPagination nbPages={nbPages} clickChangePage={clickChangePage} />
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

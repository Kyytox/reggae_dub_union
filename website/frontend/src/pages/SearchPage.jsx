import { useParams } from "react-router-dom";
import AudioPlayer from "../components/AudioPlayer";
import SectionFilter from "../components/SectionFilter";
import useVinylsData from "../requests/UseVinylsData";

import ResultEmpty from "../errors/ResultEmpty";

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

export default SearchPage;

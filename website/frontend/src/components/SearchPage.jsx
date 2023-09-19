import { useContext, useEffect, useState } from "react";
import { AuthContext } from "./AuthContext";
import { getAxios, getAxiosAuth } from "./UtilsAxios";
import { useParams } from "react-router-dom";
import AudioPlayer from "./AudioPlayer";
import LstShops from "./LstShops";
import LstFormatVinyls from "./LstFormatVinyls";
import "../App.css";

function SearchPage() {
    const { search } = useParams();

    const { isLoggedIn, idUser } = useContext(AuthContext);
    const [lstShops, setLstShops] = useState([]);
    const [lstShopsSelected, setLstShopsSelected] = useState([]);
    const [lstFormatVinyls, setLstFormatVinyls] = useState([]);
    const [lstFormatVinylsSelected, setLstFormatVinylsSelected] = useState([]);
    const [lstSearch, setLstSearch] = useState([]);
    const [lstSearchSelected, setLstSearchSelected] = useState([]);
    const [lstFavoris, setLstFavoris] = useState([]);
    const [topSearch, setTopSearch] = useState(false);

    const FetchData = async () => {
        try {
            console.log("Fetching data...");

            // get data
            if (isLoggedIn) {
                const favoris = await getAxiosAuth("/get_favoris", idUser);
                if (favoris === "Token is not valid") {
                    logout();
                    navigate("/login");
                }
                setLstFavoris(favoris);
            }

            const search_response = await getAxios("/search/" + search);

            if (search_response.length === 0) {
                setTopSearch(true);
            }

            getUniqueShops(search_response);
            getUniqueFormatVinyls(search_response);
            setLstSearch(search_response);
            setLstSearchSelected(search_response);
        } catch (error) {
            console.error("Une erreur s'est produite :", error);
        }
    };

    // get Vinyls and Songs
    useEffect(() => {
        FetchData();
    }, []);

    useEffect(() => {
        // get all vinyls from selected shops, if no shop is selected, get all vinyls
        const newLstVinyls =
            lstShopsSelected.length === 0
                ? lstSearch
                : lstSearch.filter((vinyl) =>
                      lstShopsSelected.includes(vinyl.site)
                  );

        // filter by selected format vinyls, if any
        const filteredLstVinyls =
            lstFormatVinylsSelected.length === 0
                ? newLstVinyls
                : newLstVinyls.filter((vinyl) =>
                      lstFormatVinylsSelected.includes(vinyl.format)
                  );

        setLstSearchSelected(filteredLstVinyls);

        getUniqueFormatVinyls(newLstVinyls);
    }, [lstShopsSelected, lstFormatVinylsSelected]);

    const getUniqueFormatVinyls = (lst) => {
        const lstFormatVinyls = lst
            .map((vinyl) => vinyl.format)
            .filter((value, index, self) => self.indexOf(value) === index);
        setLstFormatVinyls(lstFormatVinyls);
    };
    const getUniqueShops = (lst) => {
        const lstShops = lst
            .map((vinyl) => vinyl.site)
            .filter((value, index, self) => self.indexOf(value) === index)
            .map((shop) => {
                return { name: shop };
            });
        setLstShops(lstShops);
    };

    return (
        <div className="home">
            {topSearch ? (
                <div className="noResult" style={{ marginTop: "5em" }}>
                    <h2>No result found for "{search}"</h2>
                </div>
            ) : (
                <>
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
                        lstSongs={lstSearchSelected}
                        lstFavoris={lstFavoris}
                        setLstFavoris={setLstFavoris}
                        loadMoreData={null}
                    />
                </>
            )}
        </div>
    );
}

export default SearchPage;

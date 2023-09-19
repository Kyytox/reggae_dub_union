import { useContext, useEffect, useState } from "react";
import { AuthContext } from "./AuthContext";
import { useNavigate } from "react-router-dom";
import { getAxiosAuth } from "./UtilsAxios";
import AudioPlayer from "./AudioPlayer";
import LstShops from "./LstShops";
import LstFormatVinyls from "./LstFormatVinyls";
import "../App.css";

function Favoris() {
    const navigate = useNavigate();
    const { isLoggedIn, idUser, logout } = useContext(AuthContext);
    const [lstShops, setLstShops] = useState([]);
    const [lstShopsSelected, setLstShopsSelected] = useState([]);
    const [lstFormatVinyls, setLstFormatVinyls] = useState([]);
    const [lstFormatVinylsSelected, setLstFormatVinylsSelected] = useState([]);
    const [lstFavoris, setLstFavoris] = useState([]);
    const [lstFavorisSelected, setLstFavorisSelected] = useState([]);

    const FetchData = async () => {
        try {
            console.log("Fetching data...");

            // get data
            console.log("isLoggedIn", isLoggedIn, idUser);
            if (isLoggedIn) {
                const favoris = await getAxiosAuth("/get_favoris", idUser);
                if (favoris === "Token is not valid") {
                    logout();
                    navigate("/login");
                }
                getUniqueShops(favoris);
                getUniqueFormatVinyls(favoris);
                setLstFavoris(favoris);
                setLstFavorisSelected(favoris);
            } else {
                navigate("/login");
            }
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
                ? lstFavoris
                : lstFavoris.filter((vinyl) =>
                      lstShopsSelected.includes(vinyl.site)
                  );

        // filter by selected format vinyls, if any
        const filteredLstVinyls =
            lstFormatVinylsSelected.length === 0
                ? newLstVinyls
                : newLstVinyls.filter((vinyl) =>
                      lstFormatVinylsSelected.includes(vinyl.format)
                  );

        setLstFavorisSelected(filteredLstVinyls);

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
                lstSongs={lstFavorisSelected}
                lstFavoris={lstFavoris}
                setLstFavoris={setLstFavoris}
                loadMoreData={null}
            />
        </div>
    );
}

export default Favoris;

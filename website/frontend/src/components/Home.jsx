import { useContext, useEffect, useState } from "react";
import { AuthContext } from "./AuthContext";
import { getAxios, getAxiosAuth } from "./UtilsAxios";
import AudioPlayer from "./AudioPlayer";
import LstShops from "./LstShops";
import LstFormatVinyls from "./LstFormatVinyls";
import "../App.css";

function Home() {
    const { isLoggedIn, idUser } = useContext(AuthContext);
    const nbVinyls = 100;
    const [lstVinyls, setLstVinyls] = useState([]);
    const [lstVinylsSelected, setLstVinylsSelected] = useState([]);
    const [lstShops, setLstShops] = useState([]);
    const [lstShopsSelected, setLstShopsSelected] = useState([]);
    const [lstFormatVinyls, setLstFormatVinyls] = useState([]);
    const [lstFormatVinylsSelected, setLstFormatVinylsSelected] = useState([]);
    const [lstFavoris, setLstFavoris] = useState([]);

    const FetchData = async () => {
        try {
            console.log("Fetching data...");

            // get data
            const vinyls = await getAxios("/get_vinyls_songs");
            const shops = await getAxios("/get_shops");
            if (isLoggedIn) {
                const favoris = await getAxiosAuth("/get_favoris", idUser);
                if (favoris === "Token is not valid") {
                    logout();
                    navigate("/login");
                }
                setLstFavoris(favoris);
            }

            // update States
            setLstShops(shops);
            getUniqueFormatVinyls(vinyls);
            setLstVinyls(vinyls);
            // recup 300 first vinyls
            setLstVinylsSelected(vinyls.slice(0, nbVinyls));
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
                ? lstVinyls
                : lstVinyls.filter((vinyl) =>
                      lstShopsSelected.includes(vinyl.site)
                  );

        // filter by selected format vinyls, if any
        const filteredLstVinyls =
            lstFormatVinylsSelected.length === 0
                ? newLstVinyls
                : newLstVinyls.filter((vinyl) =>
                      lstFormatVinylsSelected.includes(vinyl.format)
                  );

        setLstVinylsSelected(filteredLstVinyls.slice(0, nbVinyls));

        getUniqueFormatVinyls(newLstVinyls);
    }, [lstShopsSelected, lstFormatVinylsSelected]);

    const getUniqueFormatVinyls = (lstVinyls) => {
        const lstFormatVinyls = lstVinyls
            .map((vinyl) => vinyl.format)
            .filter((value, index, self) => self.indexOf(value) === index);
        setLstFormatVinyls(lstFormatVinyls);
    };

    const loadMoreData = () => {
        // collect last id of lstVinylsSelected
        const lastId = lstVinylsSelected[lstVinylsSelected.length - 1].id;

        // get 200 vinyls after lastId (inferior to lastId)
        const newLstVinyls = lstVinyls
            .filter((vinyl) => vinyl.id < lastId)
            .slice(0, nbVinyls);

        // append newLstVinyls to lstVinylsSelected
        setLstVinylsSelected([...lstVinylsSelected, ...newLstVinyls]);
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
                lstSongs={lstVinylsSelected}
                lstFavoris={lstFavoris}
                setLstFavoris={setLstFavoris}
                loadMoreData={loadMoreData}
            />
        </div>
    );
}

export default Home;

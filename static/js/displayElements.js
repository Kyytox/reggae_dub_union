// display all Vinyls
var topAllVinyls = document.querySelector("#top-all-vinyls").innerHTML;
if (topAllVinyls === "True") {
    document.getElementById("btn-see-all").style.display = "none";
    displayPlayerAudio();
}

function displayPlayerAudio() {
    var divPlayerShop = document.getElementById("div-player-shops");
    var reduceMain = document.getElementById("main-app");
    var divPlayer = document.getElementById("div-player");
    var divShop = document.getElementById("div-shop-lst");
    var divSearch = document.getElementById("div-search-bar");

    if (divPlayerShop.className.includes("inactive")) {
        console.log("test");
        // display div Player Shop
        divPlayerShop.classList.remove("inactive");
        divPlayerShop.classList.add("active");

        // display player audio
        divPlayer.classList.add("active");
        divPlayer.classList.remove("inactive");

        // reduce main
        reduceMain.classList.add("reduce");
    } else if (!divShop.className.includes("inactive")) {
        // display div Player
        divPlayer.classList.remove("inactive");
        divPlayer.classList.add("active");

        // hide search bar
        divSearch.classList.remove("active");
        divSearch.classList.add("inactive");
    } else {
        console.log("test");
        // display player audio
        divPlayer.classList.add("active");
        divPlayer.classList.remove("inactive");

        // reduce main
        reduceMain.classList.add("reduce");

        // hide search bar
        divSearch.classList.remove("active");
        divSearch.classList.add("inactive");
    }
}

function displaySearchBar() {
    var divPlayerShop = document.getElementById("div-player-shops");
    var reduceMain = document.getElementById("main-app");
    var divPlayer = document.getElementById("div-player");
    var divSearch = document.getElementById("div-search-bar");

    if (divPlayerShop.className.includes("inactive")) {
        divPlayerShop.classList.remove("inactive");
        divPlayerShop.classList.add("active");

        reduceMain.classList.add("reduce");

        divSearch.classList.remove("inactive");
        divSearch.classList.add("active");
    } else if (!divPlayer.className.includes("inactive")) {
        // hide player audio
        divPlayer.classList.remove("active");
        divPlayer.classList.add("inactive");

        // display list Shops
        divSearch.classList.remove("inactive");
        divSearch.classList.add("active");
    } else {
        // display list Shops
        divSearch.classList.remove("inactive");
        divSearch.classList.add("active");
    }
}

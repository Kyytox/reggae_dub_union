function displayPlayerAudio() {
    var divPlayerShop = document.getElementById("div-player-shops");
    var reduceMain = document.getElementById("main-app");
    var divPlayer = document.getElementById("div-player");
    var divShop = document.getElementById("div-shop-lst");

    if (divPlayerShop.className.includes("inactive")) {
        // display div Player Shop
        divPlayerShop.classList.remove("inactive");
        divPlayerShop.classList.add("active");

        // display player audio
        divPlayer.classList.add("active");
        divPlayer.classList.remove("inactive");

        // reduce main
        reduceMain.classList.add("reduce");
    } else if (divShop.className.includes("active")) {
        divShop.classList.remove("active");
        divShop.classList.add("inactive");

        // display div Player
        divPlayer.classList.remove("inactive");
        divPlayer.classList.add("active");
    }
}

function displayShops() {
    var divPlayerShop = document.getElementById("div-player-shops");
    var reduceMain = document.getElementById("main-app");
    var divPlayer = document.getElementById("div-player");
    var divShop = document.getElementById("div-shop-lst");

    if (divPlayerShop.className.includes("inactive")) {
        divPlayerShop.classList.remove("inactive");
        divPlayerShop.classList.add("active");

        reduceMain.classList.add("reduce");

        divPlayer.classList.add("inactive");

        divShop.classList.remove("inactive");
        divShop.classList.add("active");
    } else if (divPlayer.className.includes("active")) {
        // hide player audio
        divPlayer.classList.remove("active");
        divPlayer.classList.add("inactive");

        // display list Shops
        divShop.classList.remove("inactive");
        divShop.classList.add("active");
    }
}

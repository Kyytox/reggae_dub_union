function add_favoris(index) {
    if (document.URL.slice(-1) === "/") {
        formatUrlCurr = "0";
        shopUrlCurr = "home";
    } else {
        // collect format in url of page
        var formatUrlCurr = document.URL.split("%").pop().replace("20", "");

        // collect name shop in url of page
        var shopUrlCurr = document.URL.split("%")[0].split("/").pop().replace(",", "");
    }

    var btnFavoris = document.getElementById("btn-fav" + " " + "btn_add_favoris-" + index);
    if (btnFavoris.className.includes("added")) {
        console.log("supp");
        action_fav = "supp";
        btnFavoris.style.color = "white";
        btnFavoris.classList.remove("added");
    } else {
        action_fav = "add";
        btnFavoris.style.color = "#bae400";
        btnFavoris.classList.add("added");
    }

    $.ajax({
        type: "POST",
        url: "/favoris_post",
        data: {
            shop: shop[index].innerText,
            title: titlevinyl[index].innerText,
            image: imgvinyl[index].innerText,
            url: urlvinyl[index].innerText,
            song: titlemp3[index].innerText,
            file: urlmp3[index].innerText,
            action: action_fav,
            shop: shopUrlCurr,
            format: formatUrlCurr,
        },
    });
}

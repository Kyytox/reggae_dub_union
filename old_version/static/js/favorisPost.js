function add_favoris(index) {
    var btnFavoris = document.getElementById("btn-fav" + " " + "btn_add_favoris-" + index);
    if (btnFavoris.className.includes("added")) {
        console.log("supp");
        action_fav = "supp";
        btnFavoris.style.color = "white";
        btnFavoris.classList.remove("added");
    } else {
        action_fav = "add";
        btnFavoris.style.color = "#ce0000";
        btnFavoris.classList.add("added");
    }

    $.ajax({
        type: "POST",
        url: "/favoris_post",
        data: {
            shop: shop[index].innerText,
            format: format[index].innerText,
            title: titlevinyl[index].innerText,
            image: imgvinyl[index].innerText,
            url: urlvinyl[index].innerText,
            song: titlemp3[index].innerText,
            file: urlmp3[index].innerText,
            action: action_fav,
        },
    });
}

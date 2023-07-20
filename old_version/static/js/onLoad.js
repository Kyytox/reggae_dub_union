// There actions start when page is load

// remplace heart by xMark if we are in page favoris
var urlCurrent = document.location.href;
if (urlCurrent.search("favoris") != -1) {
    console.log("la");
    const btn_supp = document.querySelectorAll(".fa-heart");
    for (let i = 1; i < btn_supp.length; i++) {
        btn_supp[i].classList.remove("fa-heart");
        btn_supp[i].classList.add("fa-xmark");
        btn_supp[i].classList.add("added");
        btn_supp[i].style.color = "#bae400";
    }
} else if (urlCurrent.search("signup") != -1 || urlCurrent.search("login") != -1) {
    console.log("ici");
    // it's login / signUp page
    // don't display icones navbar
    document.querySelector(".fa-magnifying-glass").style.display = "none";
    document.querySelector(".fa-music").style.display = "none";
    document.querySelector(".fa-folder").style.display = "none";
}

// display = none if user is not connect
if (!document.querySelector("#name-user-connect")) {
    const box = document.querySelectorAll(".fa-heart");
    for (let i = 0; i < box.length - 1; i++) {
        box[i].style.display = "none";
    }
}

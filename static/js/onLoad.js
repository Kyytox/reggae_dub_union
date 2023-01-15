// There actions start when page is load

// remplace heart by xMark if we are in page favoris
var urlcourante = document.location.href;
if (urlcourante.search("favoris") != -1) {
    const btn_supp = document.querySelectorAll(".fa-heart");
    for (let i = 1; i < btn_supp.length; i++) {
        btn_supp[i].classList.remove("fa-heart");
        btn_supp[i].classList.add("fa-xmark");
        btn_supp[i].classList.add("added");
        btn_supp[i].style.color = "#bae400";
    }
}

// display = none if user is not connect
if (!document.querySelector("#name-user-connect")) {
    const box = document.querySelectorAll(".fa-heart");
    for (let i = 0; i < box.length - 1; i++) {
        box[i].style.display = "none";
    }
}

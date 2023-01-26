function createTrackItem(index, title, song, image, urlvinyl) {
    var trackItem = document.createElement("div");
    trackItem.setAttribute("class", "playlist-track-ctn");
    trackItem.setAttribute("id", "ptc-" + index);
    trackItem.setAttribute("data-index", index);
    document.querySelector(".playlist-ctn").appendChild(trackItem);

    var songImg = document.createElement("div");
    songImg.setAttribute("class", "playlist-song-img");
    songImg.setAttribute("id", "img-" + index);
    songImg.setAttribute("data-index", index);
    document.querySelector("#ptc-" + index).appendChild(songImg);

    var img = document.createElement("img");
    img.setAttribute("class", "fas fa-img");
    img.setAttribute("id", "s-img-" + index);
    img.setAttribute("data-index", index);
    img.setAttribute("src", image);
    img.setAttribute("alt", title + "-" + song);
    // display img err if url image is not valid
    img.onerror = function () {
        img.setAttribute("src", "static/img/image-err.jpg");
    };
    document.querySelector("#img-" + index).appendChild(img);

    var trackInfoItem = document.createElement("div");
    trackInfoItem.setAttribute("class", "playlist-info-track");
    trackInfoItem.setAttribute("id", "pit-" + index);
    trackInfoItem.setAttribute("data-index", index);
    document.querySelector("#ptc-" + index).appendChild(trackInfoItem);

    var trackInfoItemTitle = document.createElement("h5");
    trackInfoItemTitle.setAttribute("class", "playlist-info-track-title");
    trackInfoItemTitle.setAttribute("data-index", index);
    trackInfoItemTitle.innerHTML = title;
    document.querySelector("#pit-" + index).appendChild(trackInfoItemTitle);

    var trackInfoItemName = document.createElement("h3");
    trackInfoItemName.setAttribute("class", "playlist-info-track-name");
    trackInfoItemName.setAttribute("data-index", index);
    trackInfoItemName.innerHTML = song;
    document.querySelector("#pit-" + index).appendChild(trackInfoItemName);

    var playBtnItem = document.createElement("div");
    playBtnItem.setAttribute("class", "playlist-btn-play");
    playBtnItem.setAttribute("id", "pbp-" + index);
    playBtnItem.setAttribute("data-index", index);
    document.querySelector("#ptc-" + index).appendChild(playBtnItem);

    // Button Favoris
    var trackBtnAddFavoris = document.createElement("i");
    trackBtnAddFavoris.setAttribute("id", "btn-fav" + " " + "btn_add_favoris-" + index);
    trackBtnAddFavoris.setAttribute("class", "fa-solid fa-heart");
    trackBtnAddFavoris.setAttribute("style", "display:block; color:white");
    trackBtnAddFavoris.setAttribute("data-index", index);
    trackBtnAddFavoris.addEventListener("click", function () {
        add_favoris(index);
    });
    trackBtnAddFavoris.content = "";
    document.querySelector("#ptc-" + index).appendChild(trackBtnAddFavoris);

    // Link vinyls
    var trackBtnLink = document.createElement("a");
    trackBtnLink.setAttribute("id", "btv-" + index);
    trackBtnLink.setAttribute("class", "btn_link_vinyl");
    trackBtnLink.setAttribute("style", "display:block; color:white");
    trackBtnLink.setAttribute("href", urlvinyl);
    trackBtnLink.setAttribute("target", "_blank");
    trackBtnLink.setAttribute("rel", "noopener noreferrer");
    trackBtnLink.setAttribute("data-index", index);
    document.querySelector("#ptc-" + index).appendChild(trackBtnLink);

    var trackImgLink = document.createElement("i");
    trackBtnLink.setAttribute("class", "fa-solid fa-arrow-up-right-from-square");
    document.querySelector("#btv-" + index).appendChild(trackImgLink);
}

var listAudio = [];
let shop = document.querySelectorAll("#shop-name"); //collect all shop name of page
let format = document.querySelectorAll("#format-vinyl"); //collect all format vinyl
let titlevinyl = document.querySelectorAll("#titre-vinyl"); //collect all title vinyls of page
let imgvinyl = document.querySelectorAll("#img-vinyl"); //collect img duration mp3 of page
let urlvinyl = document.querySelectorAll("#url-vinyl"); //collect all url vinyls of page
let titlemp3 = document.querySelectorAll("#mp3-title-song"); //collect all title mp3 of page
let urlmp3 = document.querySelectorAll("#mp3-url-song"); //collect all url mp3 of page

for (let i = 0; i < titlemp3.length; i++) {
    listAudio.push({
        shop: shop[i].innerText,
        format: format[i].innerText,
        title: titlevinyl[i].innerText,
        image: imgvinyl[i].innerText,
        url: urlvinyl[i].innerText,
        song: titlemp3[i].innerText,
        file: urlmp3[i].innerText,
    });
}

for (var i = 0; i < listAudio.length; i++) {
    createTrackItem(i, listAudio[i].title, listAudio[i].song, listAudio[i].image, listAudio[i].url);
}
var indexAudio = 0;

function loadNewTrack(index) {
    var player = document.querySelector("#source-audio");
    player.src = listAudio[index].file;
    document.querySelector(".img").src = listAudio[index].image;
    document.querySelector(".img").alt = listAudio[index].title + "-" + listAudio[index].song;
    document.querySelector(".img").onerror = function () {
        document.querySelector(".img").src = "static/img/image-err.jpg";
    };
    document.querySelector(".url-vinyl").href = listAudio[index].url;
    document.querySelector(".title").innerHTML = listAudio[index].title;
    document.querySelector(".song").innerHTML = listAudio[index].song;
    document.querySelector("#shop-name-h3").innerText = listAudio[index].shop;

    this.currentAudio = document.getElementById("myAudio");
    this.currentAudio.load();
    this.toggleAudio();
    this.updateStylePlaylist(this.indexAudio, index);
    this.indexAudio = index;
}

var playListItems = document.querySelectorAll(".playlist-track-ctn");

for (let i = 0; i < playListItems.length; i++) {
    playListItems[i].addEventListener("click", getClickedElement.bind(this));
}

function getClickedElement(event) {
    console.log("event.target.classList.value", event.target.classList.value.includes("heart"));
    // if not click on btn-fav or btn-link load track
    if (!event.target.classList.value.includes("heart") && !event.target.classList.value.includes("square") && !event.target.classList.value.includes("xmark")) {
        console.log("display");
        displayPlayerAudio();

        // collet index of element and load new track
        var clickedIndex = event.target.getAttribute("data-index");
        if (clickedIndex == this.indexAudio) {
            // alert('Same audio');
            this.toggleAudio();
        } else {
            loadNewTrack(clickedIndex);
        }
    }
}

// Load first track in Player Audio
document.querySelector("#source-audio").src = listAudio[indexAudio].file;
document.querySelector(".img").src = listAudio[indexAudio].image;
document.querySelector(".img").alt = listAudio[indexAudio].title + "-" + listAudio[indexAudio].song;
document.querySelector(".img").onerror = function () {
    document.querySelector(".img").src = "static/img/image-err.jpg";
};
document.querySelector(".url-vinyl").href = listAudio[indexAudio].url;
document.querySelector(".title").innerHTML = listAudio[indexAudio].title;
document.querySelector(".song").innerHTML = listAudio[indexAudio].song;
document.querySelector("#shop-name-h3").innerText = listAudio[indexAudio].shop;

// Add Button Favoris
var playerFavoris = document.createElement("i");
playerFavoris.setAttribute("id", "btn_favori");
playerFavoris.setAttribute("class", "fa-solid fa-heart");
playerFavoris.setAttribute("style", "display:block");
playerFavoris.addEventListener("click", function () {
    add_favoris(index);
});
playerFavoris.content = "";

if (document.getElementById("btn_favori")) {
    var oldBtnFav = document.getElementsByClassName("btn-favoris").children[0];
    oldBtnFav.replaceChild(playerFavoris, oldBtnFav[0]);
} else {
    document.querySelector(".btn-favoris").appendChild(playerFavoris);
}

var currentAudio = document.getElementById("myAudio");

currentAudio.load();

currentAudio.onloadedmetadata = function () {
    document.getElementsByClassName("duration")[0].innerHTML = this.getMinutes(this.currentAudio.duration);
}.bind(this);

var interval1;

function toggleAudio() {
    if (this.currentAudio.paused) {
        document.querySelector("#icon-play").style.display = "none";
        document.querySelector("#icon-pause").style.display = "block";
        document.querySelector("#ptc-" + this.indexAudio).classList.add("active-track");
        document.querySelector(".img").classList.add("active");
        this.currentAudio.volume = 0.6;
        this.currentAudio.play();
    } else {
        document.querySelector("#icon-play").style.display = "block";
        document.querySelector("#icon-pause").style.display = "none";
        document.querySelector(".img").classList.remove("active");
        this.pauseToPlay(this.indexAudio);
        this.currentAudio.pause();
    }
}

function pauseAudio() {
    this.currentAudio.pause();
    clearInterval(interval1);
}

var timer = document.getElementsByClassName("timer")[0];

var barProgress = document.getElementById("myBar");

var width = 0;

function onTimeUpdate() {
    var t = this.currentAudio.currentTime;
    timer.innerHTML = this.getMinutes(t);
    this.setBarProgress();
    if (this.currentAudio.ended) {
        document.querySelector("#icon-play").style.display = "block";
        document.querySelector("#icon-pause").style.display = "none";
        this.pauseToPlay(this.indexAudio);
        if (this.indexAudio < listAudio.length - 1) {
            var index = parseInt(this.indexAudio) + 1;
            this.loadNewTrack(index);
        }
    }
}

function setBarProgress() {
    var progress = (this.currentAudio.currentTime / this.currentAudio.duration) * 100;
    document.getElementById("myBar").style.width = progress + "%";
}

function getMinutes(t) {
    var min = parseInt(parseInt(t) / 60);
    var sec = parseInt(t % 60);
    if (sec < 10) {
        sec = "0" + sec;
    }
    if (min < 10) {
        min = "0" + min;
    }
    return min + ":" + sec;
}

var progressbar = document.querySelector("#myProgress");
progressbar.addEventListener("click", seek.bind(this));

function seek(event) {
    var percent = event.offsetX / progressbar.offsetWidth;
    this.currentAudio.currentTime = percent * this.currentAudio.duration;
    barProgress.style.width = percent * 100 + "%";
}

function forward() {
    this.currentAudio.currentTime = this.currentAudio.currentTime + 10;
    this.setBarProgress();
}

function rewind() {
    this.currentAudio.currentTime = this.currentAudio.currentTime - 10;
    this.setBarProgress();
}

function next() {
    if (this.indexAudio < listAudio.length - 1) {
        var oldIndex = this.indexAudio;
        this.indexAudio++;
        updateStylePlaylist(oldIndex, this.indexAudio);
        this.loadNewTrack(this.indexAudio);
    }
}

function previous() {
    if (this.indexAudio > 0) {
        var oldIndex = this.indexAudio;
        this.indexAudio--;
        updateStylePlaylist(oldIndex, this.indexAudio);
        this.loadNewTrack(this.indexAudio);
    }
}

function updateStylePlaylist(oldIndex, newIndex) {
    document.querySelector("#ptc-" + oldIndex).classList.remove("active-track");
    this.pauseToPlay(oldIndex);
    document.querySelector("#ptc-" + newIndex).classList.add("active-track");
    document.querySelector(".img").classList.add("active");
}

function pauseToPlay(index) {
    currentAudio.volume = 0.6;
}

function toggleMute() {
    var volUp = document.querySelector("#icon-vol-up");
    var volMute = document.querySelector("#icon-vol-mute");
    if (this.currentAudio.muted == false) {
        this.currentAudio.muted = true;
        volUp.style.display = "none";
        volMute.style.display = "block";
    } else {
        this.currentAudio.muted = false;
        volMute.style.display = "none";
        volUp.style.display = "block";
    }
}

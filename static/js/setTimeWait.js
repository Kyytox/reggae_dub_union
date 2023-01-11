function setTimeWait(nameShop) {
    console.log("testestesteste", nameShop);
    var TimeWait = parseInt(document.querySelector("#time-wait").innerHTML);
    console.log("time wait :", TimeWait);

    const shop = nameShop;
    switch (shop) {
        case "jahwaggysrecords":
            TimeWait += 1;
            break;
        case "controltowerrecords":
            if (document.getElementById(nameShop).checked) {
                TimeWait += 1;
            } else {
                TimeWait -= 1;
            }
            break;
        case "onlyrootsreggae":
            TimeWait += 1;
            break;
        case "reggaefever":
            TimeWait += 1;
            break;
        case "deeprootsreggae":
            TimeWait += 1;
            break;
        case "rastavibes":
            TimeWait += 1;
            break;
        case "pataterecords":
            TimeWait += 1;
            break;
        case "toolboxrecords":
            TimeWait += 1;
            break;
        case "lionvibes":
            TimeWait += 1;
            break;
        case "reggaemuseum":
            TimeWait += 1;
            break;
    }
    document.querySelector("#time-wait").innerHTML = TimeWait.toString();
}

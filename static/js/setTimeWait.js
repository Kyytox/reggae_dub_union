function setTimeWait(nameShop) {
    console.log("testestesteste", nameShop);
    var TimeWait = parseInt(document.querySelector("#time-wait").innerHTML);
    console.log("time wait :", TimeWait);

    const shop = nameShop;
    switch (shop) {
        case "jahwaggysrecords":
            TimeWait += ischeck(nameShop, 45);
            break;
        // case "controltowerrecords":
        //     TimeWait += ischeck(nameShop, 7);
        //     break;
        case "onlyrootsreggae":
            TimeWait += ischeck(nameShop, 7);
            break;
        case "reggaefever":
            TimeWait += ischeck(nameShop, 1);
            break;
        case "deeprootsreggae":
            TimeWait += ischeck(nameShop, 25);
            break;
        case "pataterecords":
            TimeWait += ischeck(nameShop, 22);
            break;
        case "toolboxrecords":
            TimeWait += ischeck(nameShop, 5);
            break;
        case "lionvibes":
            TimeWait += ischeck(nameShop, 1);
            break;
        case "reggaemuseum":
            TimeWait += ischeck(nameShop, 1);
            break;
    }
    document.querySelector("#time-wait").innerHTML = TimeWait.toString();
}

function ischeck(nameShop, time) {
    if (document.getElementById(nameShop).checked) {
        return time;
    } else {
        return -time;
    }
}

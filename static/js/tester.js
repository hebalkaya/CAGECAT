console.log("We logged something")

function enableOrDisableOption(id, enable) {
    // For checkboxes
    var elem = document.getElementById(id);

    elem.checked = enable;
    elem.disabled = !enable;
}

function option5change(){
    var elem = document.getElementById("option5")
    var enable = !elem.checked

    enableOrDisableOption("option1", enable);
    enableOrDisableOption("option2", enable);
}

function validateForm(){
    var x = document.forms["optionForm"]["e-value"];
    console.log(x.value);
    // TODO

    return true; // Accepts form (and therefore continues to next page if true
    // is returned)
}
function changeFooterVisibility(){
    var elem = document.getElementById("showFooterCheckbox");
    // var footer = document.getElementById("custom_footer");
    //console.log(elem);
    // console.log($("custom_footer"));

    var footer = $("#custom_footer"); // uses ID
    let speed = "slow"
    if (!elem.checked) {
        footer.slideUp(speed);
    }
    else {
        footer.slideDown(speed)
    }

}

function toggleElementVisibility(id) {
    var elem = document.getElementById(id);

    if (elem.style.display === "none") {
        elem.style.display = "block";
    } else {
        elem.style.display = "none";
    }
}


// When option 5 becomes checked: uncheck option 1 and 2, and make them unclickable
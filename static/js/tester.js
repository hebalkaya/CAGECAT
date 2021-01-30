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

    return false;
}

// When option 5 becomes checked: uncheck option 1 and 2, and make them unclickable
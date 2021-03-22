var ncbiPattern = "^[A-Z]{3}(\\d{5}|\\d{7})(\\.\\d{1,3})? *$"
// Examples: "ABC12345", "ABC9281230.999", "PAK92813.22" up to .999th version
var jobIDPattern = "^([A-Z]\\d{3}){3}[A-Z]\\d{2}$"
var selectedClusters = []


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
    // TODO

    return validateNCBIEntries();
    // Is now executed twice: when submitting the form, and onfocusout of text area
    // Accepts form (and therefore continues to next page if true
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

function toggleDisabled(id){
    var elem = document.getElementById(id);

    if (elem.disabled === false){
        removeRequiredAndEnabled(id);
    }
    else {
        setRequiredAndEnabled(id);
    }
}

function setRequiredAndEnabled(id){
    document.getElementById(id).setAttribute('required', 'required');
    document.getElementById(id).removeAttribute('disabled');
}

function removeRequiredAndEnabled(id){
    document.getElementById(id).setAttribute('disabled', 'disabled');
    document.getElementById(id).removeAttribute('required');
}

function showInputOptions(selectionOption){
    if (selectionOption === 'fasta'){
        document.getElementById('genomeFileUploadDiv').style.display = 'block';
        document.getElementById('ncbiEntriesDiv').style.display = 'none';
        document.getElementById('searchPrevJobOptions').style.display = 'none';

        // enable
        setRequiredAndEnabled('genomeFile');

        // disable elements
        removeRequiredAndEnabled('ncbiEntriesTextArea');
        removeRequiredAndEnabled('searchEnteredJobId');
        removeRequiredAndEnabled('searchUploadedSessionFile');

        enableOrDisableOption('searchSection', true);

        document.getElementById("accessionsError").style.display = "none";
        document.getElementById("submitSearchForm").removeAttribute("disabled");

    }
    else if (selectionOption === 'ncbi_entries'){
        document.getElementById('genomeFileUploadDiv').style.display = 'none';
        document.getElementById('ncbiEntriesDiv').style.display = 'block';
        document.getElementById('searchPrevJobOptions').style.display = 'none';

        // enable
        setRequiredAndEnabled('ncbiEntriesTextArea')

        // disable elements
        removeRequiredAndEnabled('genomeFile');
        removeRequiredAndEnabled('searchEnteredJobId');
        removeRequiredAndEnabled('searchUploadedSessionFile');

        enableOrDisableOption('searchSection', true);
        validateNCBIEntries();

    } else if (selectionOption === 'prev_session'){
        document.getElementById('genomeFileUploadDiv').style.display = 'none';
        document.getElementById('ncbiEntriesDiv').style.display = 'none';
        document.getElementById('searchPrevJobOptions').style.display = 'block';

        //enable
        setRequiredAndEnabled('searchEnteredJobId');

        // disable elements
        removeRequiredAndEnabled('genomeFile');
        removeRequiredAndEnabled('ncbiEntriesTextArea');

        enableOrDisableOption('searchSection', false);

        document.getElementById("accessionsError").style.display = "none";
        document.getElementById("submitSearchForm").removeAttribute("disabled");
    }
}

function showModule(ev, moduleName){
    var i, moduleSelector, moduleContent;

    moduleContent = document.getElementsByClassName('moduleContent');
    for (i=0; i < moduleContent.length; i++){
        moduleContent[i].style.display ="none";
    }

    document.getElementById(moduleName).style.display = "block";

    // Could add "active" to the moduleSelector class for better visualisation
}
function changeHitAttribute(){
    if (document.getElementById('keyFunction').value !== "len"){
        setRequiredAndEnabled('hitAttribute');
    }
    else {
        removeRequiredAndEnabled('hitAttribute');
    }
}

function changePrevSessionType(){
    let clickedButton = event.target;
    let module = clickedButton.id.split("Prev")[0];
    // console.log(module);
    let uploadSessionID = module + "UploadedSessionFile";
    let jobIDElementID = module + "EnteredJobId";

    if (clickedButton.value === "sessionFile"){
        setRequiredAndEnabled(uploadSessionID);
        removeRequiredAndEnabled(jobIDElementID);
        document.getElementById(jobIDElementID).classList.remove("invalid");
        enableOrDisableSubmitButtons(false);
    }
    else if (clickedButton.value === "jobID"){
        removeRequiredAndEnabled(uploadSessionID);
        setRequiredAndEnabled(jobIDElementID);
        validateJobID(jobIDElementID);
    }
}

function validateNCBIEntries() {
    let incorrectAcc = []
    let textArea = document.getElementById("ncbiEntriesTextArea");
    let errorBox = document.getElementById("accessionsError")
    let lines = textArea.value.split("\n");
    let valid = true;

    for (let i = 0; i < lines.length; i++) {
        if (!lines[i].match(ncbiPattern)) {
            if (lines[i] !== "") {
                incorrectAcc.push(lines[i]);
                errorBox.style.display = "block";
                valid = false;
            }
        }
    }

    if (valid) {
        textArea.classList.remove("invalid");
        errorBox.style.display = "none";
        document.getElementById("submitSearchForm").disabled = false;
    } else {
        textArea.classList.add("invalid");
        document.getElementById("accessionsErrorText").innerText = "Invalid accessions: " + incorrectAcc.join(", ");
        document.getElementById("submitSearchForm").disabled = true;
    }
    return valid;

    // example:
    // https://stackoverflow.com/questions/16465325/regular-expression-on-textarea
}

function validateJobID(target){
    let elem;
    let shouldDisable;

    if (typeof target === "undefined"){
        elem = event.target;
    }
    else {
        elem = document.getElementById(target);
    }

    if(!elem.value.match(jobIDPattern)){
        elem.classList.add("invalid");
        shouldDisable = true;
    }
    else {
        elem.classList.remove("invalid");
        shouldDisable = false;
    }
    enableOrDisableSubmitButtons(shouldDisable)
}

function enableOrDisableSubmitButtons(disable){
    let buttons = document.getElementsByClassName("submit_button");

    for (let i=0; i < buttons.length; i++){
        buttons[i].disabled = disable;
    }
}

function initializeEventHandlers(){
    let clusters = document.getElementsByClassName("result-cluster");
    for (let i=0; i < clusters.length; i++){
        // the type: "contextmenu" evaluates to a right-click of the mouse
        // and the contextmenu is not surpressed. Could be changed to a different
        // selection method in the future
        clusters[i].addEventListener("contextmenu", function(event){
            selectedClusters.push(clusters[i].value);
            console.log(selectedClusters);
        });
    }
}

// After loading, initialize
document.addEventListener('DOMContentLoaded', function() {
    initializeEventHandlers()
}, false);




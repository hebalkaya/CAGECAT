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

    // TODO: add requirement for file session or job ID
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
        // document.getElementById('ncbiEntriesTextArea').setAttribute('disabled', 'disabled');
        // document.getElementById('entered_job_id').setAttribute('disabled', 'disabled');
        // document.getElementById('uploaded_session_file').setAttribute('disabled', 'disabled');

        // document.getElementById('genomeFile').setAttribute('required', 'required');
        //
        // document.getElementById('ncbiEntriesTextArea').disabled = true;
        // document.getElementById('entered_job_id').disabled = true;
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
        // document.getElementById('genomeFile').setAttribute('disabled', 'disabled');
        // document.getElementById('entered_job_id').setAttribute('disabled', 'disabled');
        // document.getElementById('uploaded_session_file').setAttribute('disabled', 'disabled');


        // // remove required attribute
        // document.getElementById('genomeFile').removeAttribute('required');
        // document.getElementById('entered_job_id').disabled = true;
        //
        // // enable and set required attribute
        // document.getElementById('ncbiEntriesTextArea').disabled = false;
        // document.getElementById('genomeFile').setAttribute('required', 'required');


    } else if (selectionOption === 'prev_session'){
        // TODO
        document.getElementById('genomeFileUploadDiv').style.display = 'none';
        document.getElementById('ncbiEntriesDiv').style.display = 'none';
        document.getElementById('searchPrevJobOptions').style.display = 'block';

        // document.getElementById('entered_job_id').disabled = false;
        //
        // // remove attributes
        // document.getElementById('genomeFile').removeAttribute('required');
        // document.getElementById('ncbiEntriesTextArea').disabled = true;
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


// When option 5 becomes checked: uncheck option 1 and 2, and make them unclickable
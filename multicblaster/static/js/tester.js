var ncbiPattern = "^[A-Z]{3}(\\d{5}|\\d{7})(\\.\\d{1,3})? *$"
// Examples: "ABC12345", "ABC9281230.999", "PAK92813.22" up to .999th version
var jobIDPattern = "^([A-Z]\\d{3}){3}[A-Z]\\d{2}$"
var selectedClusters = []
var selectedQueries = []

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

function toggleDisabled(){
    for (let i=0; i< arguments.length; i++){
        var id = arguments[i];
        var elem = document.getElementById(id);

        if (elem.disabled === false){
            removeRequiredAndEnabled(id);
        }
        else {
            setRequiredAndEnabled(id);
        }
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
        document.getElementById("searchLabelSessionFile").classList.add("disabled");
        removeRequiredAndEnabled("searchUploadedSessionFile");

        enableOrDisableOption('searchSection', false);

        document.getElementById("accessionsError").style.display = "none";
        document.getElementById("submitSearchForm").removeAttribute("disabled");
    }
}

function showModule(ev, moduleName){
    var i, moduleSelector, moduleContent;
    // console.log(moduleName);

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
    let labelSession = module + "LabelSessionFile"

    if (clickedButton.value === "sessionFile"){
        setRequiredAndEnabled(uploadSessionID);
        document.getElementById(labelSession).classList.remove("disabled");

        removeRequiredAndEnabled(jobIDElementID);
        document.getElementById(jobIDElementID).classList.remove("invalid");
        enableOrDisableSubmitButtons(false);
    }
    else if (clickedButton.value === "jobID"){
        removeRequiredAndEnabled(uploadSessionID);
        document.getElementById(labelSession).classList.add("disabled");
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

function hasOneElementSelected(overview){
    return overview.children.length === 1 && !overview.children[0].textContent.startsWith("No");
}

function checkCorasonButton() {
    // TODO: implement that a cluster cannot be in in the cluster section and be the reference cluster at the same time
    let elem = document.getElementById("corasonSubmit");
    let queries = document.getElementById("selectedQueriesOverview");
    let clusters = document.getElementById("selectedClustersOverview")
    let referenceCluster = document.getElementById("selectedReferenceCluster");

    if (hasOneElementSelected(queries) && clusters.children.length >= 1 && !clusters.children[0].textContent.startsWith("No") && hasOneElementSelected(referenceCluster)){
        elem.removeAttribute("disabled");
    }
    else {
        elem.setAttribute("disabled", "disabled");
    }
}

window.addEventListener("message", function(e){
    let text;
    // const array;
    let src = e.data[0];
    let message = e.data[1]; // e.data represents the message posted by the child
    //
    // // -------------- TODO: check if we can generalize this function. Below
    // // -------------- was a trial, but variable referencing is not supported in JS
    // // if (src === "Clusters") {
    // //     const array = selectedClusters;
    // // }
    // // else if (src === "Queries"){
    // //     const array = selectedQueries;
    // // }
    // // else {
    // //     console.log("Invalid src type");
    // // }
    // //
    // // let index = array.indexOf(message);
    // // if (index === 1){
    // //     array.push(message);
    // // } else {
    // //     array.splice(index, 1);
    // // }
    // // if (array.length === 0){
    // //     text = "No " + src.toLowerCase() + " selected";
    // // }
    // // else {
    // //     text = array.join("\n")
    // // }
    // // document.getElementById("selected" + src + "Overview").innerText = text;
    // // ----------------------------------------------------------------------
    //
    // if (src === "Clusters"){
    //     let index = selectedClusters.indexOf(message);
    //     if (index === -1) {
    //         selectedClusters.push(message);
    //     } else {
    //         selectedClusters.splice(index, 1);
    //     }
    //     if (selectedClusters.length === 0) {
    //         text = "No clusters selected";
    //     } else {
    //         text = selectedClusters.join("\n");
    //     }
    //     document.getElementById("selectedClustersOverview").innerText = text;
    // }
    // else if (src === "Queries"){
        let resetMessage = "No " + src.toLowerCase() + " selected";
        let toRemoveIndex = undefined;

        let overview = document.getElementById("selected" + src + "Overview");

        if (overview.children[0].textContent === resetMessage ){
            overview.removeChild(overview.children[0]);
        }

        for (let i=0; i < overview.children.length; i++) {
            if (overview.children[i].textContent === message) {
                toRemoveIndex = i;
                break;
            }
        }

        if (toRemoveIndex === undefined){
            let newNode = document.createElement("LI");
            newNode.appendChild(document.createTextNode(message));

            if (src === "Clusters") {
                newNode.addEventListener("contextmenu", function (event) {
                    event.preventDefault();
                    let newOverview = document.getElementById("selectedReferenceCluster");

                    if (overview.children.length === 1 && overview.children[0].textContent !== resetMessage && this.parentElement === overview){
                        let newNode = document.createElement("LI");
                        newNode.appendChild(document.createTextNode(resetMessage));
                        overview.appendChild(newNode);
                    }

                    let newResetMessage = "No reference cluster selected";
                    if (newOverview.children[0].textContent === newResetMessage){
                        newOverview.removeChild(newOverview.children[0]);
                    }

                    if (this.parentElement === overview){
                        overview.removeChild(this);
                        newOverview.appendChild(this);
                    }
                    else {
                        if (newOverview.children.length === 1) {
                            let newNode = document.createElement("LI");
                            newNode.appendChild(document.createTextNode(newResetMessage));
                            newOverview.appendChild(newNode);
                        }

                        newOverview.removeChild(this);
                    }

                    checkCorasonButton();
                })
            }

            overview.appendChild(newNode);
        }
        else {
            overview.removeChild(overview.children[toRemoveIndex]);

            if (overview.children.length === 0){
                let newNode = document.createElement("LI");
                newNode.appendChild(document.createTextNode(resetMessage));
                overview.appendChild(newNode);
            }
        }

    checkCorasonButton()
}, false)


function loadedIframe(){
    let frame = document.getElementById("newWindow");
    let doc = frame.contentDocument || frame.contentWindow.document;
    let clusters = doc.getElementsByClassName("tickTextGroup");

    for (let i=0; i < clusters.length; i++){
        // the type: "contextmenu" evaluates to a right-click of the mouse
        // and the contextmenu is not surpressed. Could be changed to a different
        // selection method in the future
        clusters[i].addEventListener("contextmenu", function(event){
            event.preventDefault();
            let childs = clusters[i].firstChild.childNodes;
            // childs[0] represents organism and cluster # + score
            // childs[1] indicates accession number and range
            parent.window.postMessage(["Clusters", childs[0].textContent + " " + childs[1].textContent], "*");
        }); // space in line above is a non-breaking space:
            // not a regular space. " "
    }

    let ticks = doc.getElementsByClassName("tick");
    for (let i=0; i < ticks.length; i++){
        ticks[i].addEventListener("contextmenu", function(event){
            event.preventDefault();
            let query_name = ticks[i].childNodes[1];
            // console.log();
            parent.window.postMessage(["Queries", query_name.textContent], "*");
        })
    }
}


function addSelectedToForm(downstream_prog) {
    if (downstream_prog === "sequences") {
        document.getElementById("selectedQueries").value = document.getElementById("selectedQueriesOverview").innerText;
        document.getElementById("selectedClusters").value = document.getElementById("selectedClustersOverview").innerText;
    }
    else if (downstream_prog === "clusters"){
        document.getElementById("selectedClusters1").value = document.getElementById("selectedClustersOverview").innerText;
    }
    else if (downstream_prog === "corason"){
        document.getElementById("selectedQuery").value = document.getElementById("selectedQueriesOverview").innerText;
        document.getElementById("selectedClusters2").value = document.getElementById("selectedClustersOverview").innerText;
        document.getElementById("referenceCluster").value = document.getElementById("selectedReferenceCluster").innerText;
    }
    else if (downstream_prog === "clinker_full"){
        document.getElementById("selectedClustersFullClinker").value = document.getElementById("selectedClustersOverview").innerText;
    }
    else if (downstream_prog === "clinker_query"){
        document.getElementById("selectedClusters3").value = document.getElementById("selectedClustersOverview").innerText;
    }
    else {
        console.log("Invalid  type");
    }
}

function changePower(value, elemToChange){
    let elem = document.getElementById(elemToChange);
    elem.innerText = parseInt(elem.innerText) + value;
}

function mergeExponentials(){
    let allEs = ["Evalue", "Ecluster", "Ecore"]

    for (let i=0; i < allEs.length; i++){
        document.getElementById(allEs[i].toLowerCase()).value = document.getElementById("base" + allEs[i]).value + "E" + document.getElementById("power" + allEs[i]).innerText;;
    }
}

function initReadQueryFile(){
    var file = document.getElementById("genomeFile").files[0];
    if (file) {
        var reader = new FileReader();
        reader.readAsText(file, "UTF-8");
        reader.onload = function (evt) {
            console.log(evt.target.result);
            // document.getElementById("fileContents").innerHTML = evt.target.result;
        }
        reader.onerror = function (evt) {
            console.log("Error reading file");
            // document.getElementById("fileContents").innerHTML = "error reading file";
        }
    }
}

function readFileContents() {
    let headers = []
    var valid_ext = ["fasta", "fa"]
    var file = document.getElementById("genomeFile").files[0];
    var reader = new FileReader();
    let ext = file.name.split(".").pop().toLowerCase();
    reader.onload = function(evt){
        // TODO: check if file adheres to FASTA format
        if (!valid_ext.includes(ext)){
            document.getElementById("fileUploadIncorExt").style.display = "block";
            document.getElementById("fileUploadIncorExtText").innerText = "Invalid query file extension: ." + ext;
            return;
        }
        else {
            document.getElementById("fileUploadIncorExt").style.display = "none";
        }
        let splitted = reader.result.split("\n");
        for (let i=0; i<splitted.length; i++){
            // console.log("b");
            // console.log(splitted[i]);
            if (splitted[i].startsWith(">")){
                headers.push(splitted[i].slice(1, splitted[i].length));
            }
        }
        console.log(headers);
    }

    reader.readAsText(file, "UTF-8");

}
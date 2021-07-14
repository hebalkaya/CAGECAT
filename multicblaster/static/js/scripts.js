var ncbiPattern = "^[A-Z]{3}(\\d{5}|\\d{7})(\\.\\d{1,3})? *$"
// Examples: "ABC12345", "ABC9281230.999", "PAK92813.22" up to .999th version
var jobIDPattern = "^([A-Z]\\d{3}){3}[A-Z]\\d{2}$"
var selectedClusters = []
var selectedQueries = []
var currentTime = Date();
var ROOT_URL = '/multicblaster'     // TODO: must: change root if root changes

function enableOrDisableOption(id, enable) {
    // For checkboxes
    var elem = document.getElementById(id);

    elem.checked = enable;
    elem.disabled = !enable;
}

function toggleElementVisibility(id) {
    $('#'+id)[0].classList.toggle('no-display');
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

function showInputOptions(selectionOption, resetQueries){
    let genomeFileUploadDiv = $('#genomeFileUploadDiv')[0];
    let ncbiEntriesDiv = $('#ncbiEntriesDiv')[0];
    let searchPrevJobOptions = $('#searchPrevJobOptions')[0];

    if (resetQueries){
        $('#requiredSequencesSelector')[0].options.length = 0;
    }
    if (selectionOption === 'fasta'){
        genomeFileUploadDiv.classList.remove('no-display');
        ncbiEntriesDiv.classList.add('no-display');
        searchPrevJobOptions.classList.add('no-display');

        // enable
        setRequiredAndEnabled('genomeFile');

        // disable elements
        removeRequiredAndEnabled('ncbiEntriesTextArea');
        removeRequiredAndEnabled('searchEnteredJobId');
        removeRequiredAndEnabled('searchUploadedSessionFile');

        enableOrDisableOption('searchSection', true);

        document.getElementById("accessionsError").classList.add('no-display');
        document.getElementById("submitSearchForm").removeAttribute("disabled");

    }
    else if (selectionOption === 'ncbi_entries'){
        genomeFileUploadDiv.classList.add('no-display');
        ncbiEntriesDiv.classList.remove('no-display');
        searchPrevJobOptions.classList.add('no-display');

        // enable
        setRequiredAndEnabled('ncbiEntriesTextArea')

        // disable elements
        removeRequiredAndEnabled('genomeFile');
        removeRequiredAndEnabled('searchEnteredJobId');
        removeRequiredAndEnabled('searchUploadedSessionFile');

        enableOrDisableOption('searchSection', true);
        validateNCBIEntries();

    } else if (selectionOption === 'prev_session'){
        genomeFileUploadDiv.classList.add('no-display');
        ncbiEntriesDiv.classList.add('no-display');
        searchPrevJobOptions.classList.remove('no-display');

        //enable
        setRequiredAndEnabled('searchEnteredJobId');

        // disable elements
        removeRequiredAndEnabled('genomeFile');
        removeRequiredAndEnabled('ncbiEntriesTextArea');
        document.getElementById("searchLabelSessionFile").classList.add("disabled");
        removeRequiredAndEnabled("searchUploadedSessionFile");

        enableOrDisableOption('searchSection', false);

        document.getElementById("accessionsError").classList.add('no-display');
        document.getElementById("submitSearchForm").removeAttribute("disabled");

        if (!resetQueries){
            document.getElementById('radioPrevSession').setAttribute('checked', 'checked');
        }
    }
}

function showModule(ev, moduleName){
    console.log('For future tool implementation which could be a starting point')
    return;
    var i, moduleSelector, moduleContent;

    moduleContent = document.getElementsByClassName('moduleContent');
    for (i=0; i < moduleContent.length; i++){
        moduleContent[i].classList.add('no-display');
    }

    document.getElementById(moduleName).classList.remove('no-display');

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
    let correctAcc = []
    let textArea = document.getElementById("ncbiEntriesTextArea");
    let errorBox = document.getElementById("accessionsError")
    let lines = textArea.value.split("\n");
    let valid = true;
    document.getElementById("requiredSequencesSelector").options.length = 0;

    for (let i = 0; i < lines.length; i++) {
        if (!lines[i].match(ncbiPattern)) {
            if (lines[i] !== "") {
                incorrectAcc.push(lines[i]);
                errorBox.classList.remove('no-display');
                valid = false;
            }
        }

        if (correctAcc.includes(lines[i])){
            incorrectAcc.push(lines[i]);
            errorBox.classList.remove('no-display');
            valid = false;
        }

        correctAcc.push(lines[i]);
    }

    if (valid) {
        textArea.classList.remove("invalid");
        errorBox.classList.add('no-display');
        document.getElementById("submitSearchForm").disabled = false;

        let requiredSequences = document.getElementById("requiredSequencesSelector");
        let everything = textArea.value.split("\n");
        if (!(everything.length === 1 && everything[0] === "")){

            for (let i=0; i<everything.length; i++){
                if (!(everything[i] === "")){

                    // console.log(everything[i]);
                    let opt = document.createElement("option");
                    opt.text = everything[i];
                    opt.value = everything[i];
                    requiredSequences.add(opt);
                }
            }
        }



    } else {
        textArea.classList.add("invalid");
        document.getElementById("accessionsErrorText").innerText = "Invalid accessions: " + incorrectAcc.join(", ");
        document.getElementById("submitSearchForm").disabled = true;
        document.getElementById("requiredSequencesSelector").options.length = 0;
    }

    return valid;
    // example: https://stackoverflow.com/questions/16465325/regular-expression-on-textarea
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

function addSelectedToForm(downstream_prog) {
    if (downstream_prog === "sequences") {
        // document.getElementById("selectedQueries").value = document.getElementById("selectedQueriesOverview").innerText;
        // document.getElementById("selectedClusters").value = document.getElementById("selectedClustersOverview").innerText;
        // console.log(getSelectedQueries());
        // console.log($('#selectedQueriesSelector option'))
        $('#selectedQueries')[0].value = getSelectedQueries();
    }
    else if (downstream_prog === "clusters"){
        $('#selectedClusters1')[0].value = getSelectedClusters('');
        // document.getElementById("selectedClusters1").value = document.getElementById("selectedClustersOverview").innerText;
    }
    else if (downstream_prog === "corason"){
        //TODO: modify how clusters are given
        $('#selectedQuery')[0].value = getSelectedQueries();
        $('#selectedClusters2')[0].value = getSelectedClusters('');
        $('#unselectedClusters2')[0].value = getSelectedClusters('un');
        // document.getElementById("selectedQuery").value = document.getElementById("selectedQueriesOverview").innerText;
        // document.getElementById("selectedClusters2").value = document.getElementById("selectedClustersOverview").innerText;
        // document.getElementById("referenceCluster").value = document.getElementById("selectedReferenceCluster").innerText;
    }
    // else if (downstream_prog === "clinker_full"){
    //     document.getElementById("selectedClustersFullClinker").value = document.getElementById("selectedClustersOverview").innerText;
    // }
    else if (downstream_prog === "clinker_query"){

        // console.log(msg);
        $('#selectedClusters3')[0].value = getSelectedClusters();
        // document.getElementById("selectedClusters3").value = document.getElementById("selectedClustersOverview").innerText;

    }
    else {
        console.log("Invalid  type");
    }
}

// TODO: could: modularize below functions
function getSelectedClusters(prefix){
    let msg = '';
    $('#' + prefix + 'selectedClustersSelector option').each(function(){
        msg += this.innerText;
        msg += '\n'
    });
    return msg.trimEnd('\n');
}

function getSelectedQueries(){
    let msg ='';
    $('#selectedQueriesSelector option').each(function(){
        msg += this.innerText;
        msg += '\n';
    })
    return msg.trimEnd('\n');
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

function readFileContents() {
    let requiredSequencesSelect = document.getElementById("requiredSequencesSelector");
    requiredSequencesSelect.options.length = 0;  // Clear all options
    var valid_ext = ["fasta", "fa", "fsa", "fna", "faa"]
    var file = document.getElementById("genomeFile").files[0];
    var reader = new FileReader();
    let ext = file.name.split(".").pop().toLowerCase();

    reader.onload = function(evt){
        // TODO: could: check if file adheres to FASTA format
        if (!valid_ext.includes(ext)){
            document.getElementById("fileUploadIncorExt").classList.remove('no-display');
            document.getElementById("fileUploadIncorExtText").innerText = "Invalid query file extension: ." + ext;
            return;
        }
        else {
            document.getElementById("fileUploadIncorExt").classList.add('no-display');
        }
        let splitted = reader.result.split("\n");
        for (let i=0; i<splitted.length; i++){

            if (splitted[i].startsWith(">")){
                let txt = splitted[i].slice(1, splitted[i].length);
                let opt = document.createElement("option");
                opt.text = txt;
                opt.value = txt;

                requiredSequencesSelect.add(opt);
            }
        }

    }
    reader.readAsText(file, "UTF-8");
}

function addRequiredSeqs(){
    let selector = document.getElementById("requiredSequencesSelector");
    // console.log(selector.val())
    let selected = [];
    for (let i=0; i < selector.options.length; i++){
        if (selector.options[i].selected){
            selected.push(selector.options[i].value);
        }
    }
    document.getElementById("requiredSequences").value = selected.join(";");
}

function showPreviousJobs(disableBodyOnLoad){
    if (disableBodyOnLoad){
        parent.document.body.onload = null;
        // To prevent double loading as for plots the previous jobs are loaded before the big plot is loaded
    }

    let overview = document.getElementById("previousJobsOverview");

    for (let i=0; i <localStorage.length; i++){
        try{
            let jobId = localStorage.getItem(i).split(";")[0];

            let li = document.createElement("li");
            li.classList.add("jobs");

            let a = document.createElement("a");
            a.href = ROOT_URL + "/results/" + jobId;
            a.innerText = jobId;

            li.appendChild(a);
            overview.insertBefore(li, overview.childNodes[0]);
        }
        catch (error){
            console.log('Error fetching previous jobs')
            determineHeight();
            return;
        }
    }
    let li = document.createElement("li");
    let a = document.createElement("a");
    a.classList.add("no-link-decoration");
    a.href = ROOT_URL + "/results/";
    a.innerText =  "Previous jobs";
    li.appendChild(a);

    overview.insertBefore(li, overview.childNodes[0]);
}



function showHelp(textType){
    $.get(ROOT_URL + '/docs/' + textType, function(data, status){
        document.getElementById("explanationTitle").innerText = data.title;
        document.getElementById("explanationModule").innerText = "Module: " + data.module;
        document.getElementById("explanationText").innerText = data.text;
    });

    if (document.getElementById("explanationColumn").classList.contains('invisible')){
        toggleExplanationColumn();
    }
}


function toggleExplanationColumn() {
    let rightCol = document.getElementById('explanationColumn');
    let middleCol = document.getElementById('middleColumn');
    let inputs = document.getElementsByClassName('input-layer');
    let toggleButton = document.getElementById('toggleHelpButton');

    if (rightCol.classList.contains('invisible')) {
        // rightCol.classList.remove('no-display');
        rightCol.classList.remove('invisible');
        rightCol.classList.add('visible');
        middleCol.classList.add('shrink-it');
        middleCol.classList.add('enlarge-it');

        toggleButton.innerText = ">>"

    } else {
        rightCol.classList.remove('visible');
        rightCol.classList.add('invisible');
        middleCol.classList.remove('shrink-it');
        middleCol.classList.add('enlarge-it');

        toggleButton.innerText = "<<"

        // setTimeout(function(){
        //     rightCol.classList.add('no-display');
        // }, 500);
    }

    for (let i=0; i < inputs.length; i++){
        inputs[i].classList.toggle('wider-input');
        // if (wider){
        //     inputs[i].classList.add('wider-input');
        // }
        // else {
        //     inputs[i].classList.remove('wider-input');
        // }
    }

}

function determineHeight() {
    var body = document.body,
        html = document.documentElement;

    let height_tmp = Math.max(body.scrollHeight, body.offsetHeight,
        html.clientHeight, html.scrollHeight, html.offsetHeight).toString();

    let height = height_tmp - document.getElementById('navigationBar').offsetHeight - 8;
    // -8px has been found by trying

    document.getElementById('statusColumn').style.height = height + 'px';

    let explanationCol = document.getElementById('explanationColumn');
    if (explanationCol !== null) {
        explanationCol.style.height = height + 'px';
    }
}

function toggleRemoteOptions(enable){
    let individualElements = ['radioFasta', 'radioNCBIEntries', 'genomeFile', 'ncbiEntriesTextArea',
    'searchPrevJobId', 'radioPrevSession ', 'searchEnteredJobId', 'searchUploadedSessionFile'];
    let fieldsets = ['searchSectionFullFieldset', 'filteringSectionFullFieldset'];
    let sections = ['filteringSection', 'searchSection']

    for (let i=0; i < individualElements.length; i++) {
        if (document.getElementById(individualElements[i]) !== null) {
            if (enable) {
                setRequiredAndEnabled(individualElements[i]);
            } else {
                removeRequiredAndEnabled(individualElements[i]);
            }
        }
    }

    for (let i=0; i < fieldsets.length; i++){
        if (enable){
            document.getElementById(fieldsets[i]).classList.remove('no-display');
        }
        else {
            document.getElementById(fieldsets[i]).classList.add('no-display');
        }
    }

    for (let i=0; i< sections.length; i++) {
        if (enable){
            document.getElementById(sections[i]).removeAttribute('disabled');
        }
        else {
            document.getElementById(sections[i]).setAttribute('disabled', 'disabled');
        }
    }
}

function changeSearchMode(mode){
    let fieldsetDiv = document.getElementById('hmmFullFieldset');
    let fieldset = document.getElementById('hmmSection');
    let remoteOptions = document.getElementById('remoteOptionsSection');
    let radioFasta = document.getElementById('radioFasta');
    document.getElementById("requiredSequencesSelector").options.length = 0;

    if (mode === 'remote'){
        fieldsetDiv.classList.add('no-display');
        fieldset.setAttribute('disabled', 'disabled');
        remoteOptions.classList.remove('no-display');
        remoteOptions.removeAttribute('disabled');

        toggleRemoteOptions(true);
        radioFasta.click()
        document.getElementById('entrez_query').removeAttribute('disabled');
        document.getElementById('database_type').removeAttribute('disabled');

        console.log('remote');
    }
    else if (mode === 'hmm'){
        fieldsetDiv.classList.remove('no-display');
        fieldset.removeAttribute('disabled');
        remoteOptions.classList.add('no-display');
        remoteOptions.setAttribute('disabled', 'disabled');

        toggleRemoteOptions(false);
        document.getElementById('entrez_query').setAttribute('disabled', 'disabled');
        document.getElementById('database_type').setAttribute('disabled', 'disabled');

        console.log('hmm');
    }
    else if (mode === 'combi_remote'){
        fieldsetDiv.classList.remove('no-display');
        fieldset.removeAttribute('disabled');
        remoteOptions.classList.remove('no-display');
        remoteOptions.removeAttribute('disabled');

        toggleRemoteOptions(true);
        radioFasta.click()
        document.getElementById('entrez_query').removeAttribute('disabled');
        document.getElementById('database_type').removeAttribute('disabled');

        console.log('combi_remote');
    }
    else {
        console.log('Invalid mode');
    }
}

function moveSelectedElements(target, selectionType){
    let src;
    let dest;

    if (target === 'selected') {
        src = '#unselected'+ selectionType;
        dest = '#selected' + selectionType;
        // return !$('#unselectedClusters option:selected').remove().appendTo('#selectedClusters');
    }
    else if (target === 'unselected'){
        src = '#selected' + selectionType;
        dest = '#unselected' + selectionType;
    }
    else {
        console.log('Incorrect target');
    }

    let result = !$(src+'Selector' + ' option:selected').remove().appendTo(dest+ 'Selector');
    if (selectionType === 'Queries') {
        let elem = $('#corasonSubmit')[0];
        if (elem !== null) {
            if ($('#selectedQueriesSelector')[0].length === 1) {
                elem.removeAttribute('disabled');
            } else {
                elem.setAttribute('disabled', 'disabled');
            }
        }
    }

    return result;
}

function showSelection(toShow){
    // console.log($('#clusterSelection'));
    let show;
    let hide;

    if (toShow === 'cluster'){
        show = $('#clusterSelection')[0];
        hide = $('#queriesSelection')[0];
    }
    else {
        show = $('#queriesSelection')[0];
        hide = $('#clusterSelection')[0];
    }
    show.classList.remove('no-display');
    hide.classList.add('no-display');
}

function checkClanCutoffValues(){
    // TODO: still to be implemented with big-scape
    let elem = $('#clan_cutoff')[0];
    let splitted = elem.value.split(' ');

    if (parseFloat(splitted[0]) >= 0.0 && parseFloat(splitted[0]) <= 1 && parseFloat(splitted[1]) >= 0.0 && parseFloat(splitted[1]) <=1 ){
        elem.classList.remove('invalid');
    }
    else {
        elem.classList.add('invalid');
    }
}
function addClustersToUse(){
    let elem = $('#selectedReferenceCluster')[0];
    let merged = []
    // let selectedRefCluster = $('#selectedReferenceCluster')

    for (let i=0; i < elem.children.length; i++){
        if (i !== elem.selectedIndex) {
            // console.log(elem.children[i]);
            merged.push(elem.children[i].value)
        }
    }
    $('#selectedClustersToUse')[0].value = merged.join(' ');
}


document.addEventListener('scroll', function(e){
    let elem = $('#filler')[0];

    if (elem !== undefined) {
        elem.style.height = window.scrollY + 'px';
    }
})

function getOutputFromPlot(plotting_type){
    let frame = document.getElementById("newWindow");
    let doc = frame.contentDocument || frame.contentWindow.document;
    let clusters;

    let clusterSelector = $('#unselectedClustersSelector')[0];
    let querySelector = $('#unselectedQueriesSelector')[0];

    if (plotting_type === 'search'){
        clusters = doc.getElementsByClassName("tickTextGroup");

        setTimeout(function(){
            let ticks = doc.getElementsByClassName("tick");
            for (let i=0; i < ticks.length; i++){
                // // console.log(.innerHTML);
                // let qn = ticks[i].childNodes[1];
                // // timeout(0.1);
                // console.log(qn.textContent);
                const query_name = ticks[i].childNodes[1];
                // parent.window.postMessage(["Queries", query_name.textContent], "*");
                // app
                // parent.console.log();
                let text = query_name.textContent;

                let option = document.createElement('option');
                option.value = text;
                option.innerText = text;
                option.classList.add('smaller-font');

                querySelector.appendChild(option);


            }
        }, 100); // sometimes loading would fail. A timeout leads to a succesfull load
    }
    else if (plotting_type === 'visualize'){
        clusters = doc.getElementsByClassName("clusters")[0].childNodes;
    }
    else {
        console.log('Incorrect plotting type')
    }

    for (let i=0; i < clusters.length; i++) {
        let text;
        if (plotting_type === 'search') {
            text = clusters[i].firstChild.childNodes[0].textContent;

        } else if (plotting_type === 'visualize') {
            if (clusters[i].firstChild.childNodes[0].textContent !== 'Query Cluster') {
                text = clusters[i].firstChild.childNodes[0].textContent;
                // continue;
            }

        } else {
            console.log('Incorrect plotting type')
        }
        if (text !== undefined) { // in case of visualize and "Query Cluster"
            let option = document.createElement('option');
            option.value = text;
            option.innerText = text;
            option.classList.add('smaller-font');
            clusterSelector.appendChild(option);
        }
    }

    // setMultiSelectHeight();
}

// Note: functions below are labeled as unused by PyCharm (or your interpreter) but they are used
function initReadQueryFile(){ // TODO: check if this can be removed?
    var file = document.getElementById("genomeFile").files[0];
    if (file) {
        var reader = new FileReader();
        reader.readAsText(file, "UTF-8");
        reader.onload = function (evt) {
            console.log(evt.target.result);
        }

        reader.onerror = function (evt) {
            console.log("Error reading file");
        }
    }
}

function postLoadingIFrame(){
    document.getElementById("resultLoadedMessage").classList.add('fade-out');
    document.getElementById("loadingImage").classList.add('no-display');
}

function storeJobId(id, j_type, j_title){
    let maxToShow = 250;

    for (let i=0; i<maxToShow; i++){
        let str = i.toString();
        if (localStorage.getItem(str) === null){
            let msg = id + ";" + j_type + ";" + currentTime.toLocaleString() + ';' + j_title;
            console.log(msg);
            localStorage.setItem(str, msg);
            return;
        }
    }
}

function showDetailedPreviousJobs(){
    let overview = document.getElementById("detailedPreviousJobs");

    for (let i=0; i <localStorage.length; i++) {
        let msg = localStorage.getItem(i).split(";");
        let tr = document.createElement("tr");

        let td = document.createElement("td");
        let a = document.createElement("a");
        a.style = 'font-size: 17px;';
        a.classList.add('monospaced');
        a.href = ROOT_URL + "/results/" + msg[0];
        a.innerText = msg[0]
        td.appendChild(a);
        tr.appendChild(td);

        let td1 = document.createElement("td");
        td1.innerText = msg[1];
        tr.appendChild(td1);

        let td2 = document.createElement("td");
        td2.innerText = msg[2];
        tr.appendChild(td2);

        let td3 = document.createElement("td");
        td3.innerText = msg[3];
        tr.appendChild(td3);

        overview.insertBefore(tr, overview.childNodes[0]);
    }
    let tr = document.createElement("tr");

    let th = document.createElement("th");
    th.innerText = "Job ID";
    tr.appendChild(th);

    let th1 = document.createElement("th");
    th1.innerText = "Type of job";
    tr.appendChild(th1);

    let th2 = document.createElement("th");
    th2.innerText = "Date";
    tr.appendChild(th2);

    let th3 = document.createElement("th");
    th3.innerText = "Title";
    tr.appendChild(th3);

    overview.insertBefore(tr, overview.childNodes[0]);
}

function redirect(url){
    setTimeout(function(){
        window.location.href = url;
    }, 50);
}

function addAccordionListeners() {
    // from: https://www.w3schools.com/howto/howto_js_accordion.asp
    let acc = document.getElementsByClassName("accordion");

    for (let i = 0; i < acc.length; i++) {
        acc[i].addEventListener("click", function () {
            this.classList.toggle("active");
            let panel = this.nextElementSibling;
            if (panel.style.maxHeight) {
                panel.style.maxHeight = null;
            } else {
                panel.style.maxHeight = panel.scrollHeight + "px";
            }
        });
    }
}
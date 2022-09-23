function getElemById(elem_id){
    return document.getElementById(elem_id);
}

// submit
// click
// focus
// focusout

function addHelpButtonsListeners() {
    let helpButtons = document.getElementsByClassName('help-button');

    for (let i=0; i<helpButtons.length;i++){
        let elem = helpButtons[i];

        elem.addEventListener('click', function (){
            showHelp(elem.id);
        }, false);
    }
}

function addGeneralListeners(){
    let elem = getElemById('bookMarkButton');

    if (elem !== null){
        elem.addEventListener('click', function () {
            alert('Press CTRL + D to bookmark this page');
        }, false);
    }
    addHelpButtonsListeners()
}



function addCblasterSearchListeners(){
    addGeneralListeners()
    // if (module === 'search'){
    getElemById('remoteMode').addEventListener('click', function () {
        changeSearchMode('remote')
    }, false);

    getElemById('hmmMode').addEventListener('click', function (){
        changeSearchMode('hmm');
    }, false);

    getElemById('combiMode').addEventListener('click', function (){
        changeSearchMode('combi_remote');
    }, false);

    getElemById('radioFasta').addEventListener('click', function (){
        showInputOptions('file', 1);
    }, false);

    getElemById('radioNCBIEntries').addEventListener('click', function (){
        showInputOptions('ncbi_entries', 1);
    }, false);

    getElemById('searchOptionForm').addEventListener('submit',
        addRequiredSeqs, false);
    // }
    //
    // else if (module === 'recompute'){
    //
    // }


}

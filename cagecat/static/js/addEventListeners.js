function getElemById(elem_id, v){
    return document.getElementById(elem_id);
}

function addCblasterSearchListeners(){
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

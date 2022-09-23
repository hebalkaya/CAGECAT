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
            showHelp(elem.id.slice(0, -5));
        }, false);
    }
}

function addNotificationListeners(){
    addListener('base-notification', 'click', function (){
        Cookies.set('consent',1);$('#consent').remove();
    }
    )

    let notifications = document.getElementsByClassName('notification');

    for (let i=0; i<notifications.length;i++){
        let elem = notifications[i];

        elem.addEventListener('click', function(){
            Cookies.set(elem.id,1);$('#' + elem.id).remove();
        })
    }
}

function addListener(elem_id, listener_type, func){
    let elem = document.getElementById(elem_id);

    if (elem !== null){
        elem.addEventListener(listener_type, func,  false);
    }

}

function addResultPageListeners(module){
    addListener('connectedJobsToggle', 'click', function (){
        toggleElementVisibility('connectedJobs')
    });

    addListener('selectedClusterButton', 'click', function (){
        showSelection('cluster');
    });

    addListener('selectedQueryButton', 'click', function (){
        showSelection('query');
    });

    addListener('unselectClustersButton', 'click', function (){
        moveSelectedElements('unselected', 'Clusters');
    });

    addListener('selectClustersButton', 'click', function (){
        moveSelectedElements('selected', 'Clusters');
    });

    addListener('unselectQueriesButton', 'click', function (){
        moveSelectedElements('unselected', 'Queries');
    });

    addListener('selectQueriesButton', 'click', function (){
        moveSelectedElements('selected', 'Queries');
    });

    addListener('dummyIframe', 'load', function (){
        console.log('From dummyIframe');
        showPreviousJobs(true);
        console.log('From dummyIframe end');
    });

    addListener('newWindow', 'load', function (){
        console.log('From newWindow');
        if (module in ['search', 'recompute']){
            getOutputFromPlot('search')
        }
        else if (module === 'clinker_query'){
            getOutputFromPlot('visualize');
        }

        postLoadingIFrame();
        console.log('From newWindow end');
    })

}

function addExampleButtonListeners() {
    addListener('exampleInputClinker', 'click', function (){
        setExampleInput('clinker');
    })

    addListener('exampleInputCblaster', 'click', function (){
        setExampleInput('cblaster_search');
    })

    addListener('toggleHelpButton', 'click', toggleExplanationColumn);
}

function addGeneralListeners(){
    addHelpButtonsListeners();
    addNotificationListeners();
    addExampleButtonListeners();

    addListener('bookMarkButton', 'click', function () {
        alert('Press CTRL + D to bookmark this page');
    }, false);

}

function addClinkerStartPointListeners(){
    getElemById('fileUploadClinker').addEventListener('change',
        getGenBankFileNames, false);


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

    getElemById('intermediate_genes').addEventListener('click', function (){
        toggleDisabled('intermediate_max_distance', 'intermediate_max_clusters');
    }, false);

    getElemById('ncbiEntriesTextArea').addEventListener('focusout',
        validateNCBIEntries, false);

    getElemById('keyFunction').addEventListener('change',
        changeHitAttribute, false);

    getElemById('genomeFiles').addEventListener('change',
        getGenBankFileNames, false);
    // }
    //
    // else if (module === 'recompute'){
    //
    // }


}

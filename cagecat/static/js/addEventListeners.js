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

function addResultPageListeners(){
    let jobSubmissionForms = document.getElementsByClassName('downstream-form');

    for (let i=0; i<jobSubmissionForms.length;i++) {
        let elem = jobSubmissionForms[i];

        elem.addEventListener('submit', function (){
            addSelectedToForm(elem.id);
        }, false);
    }

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
        showPreviousJobs(true);
    });
}

function addExampleButtonListeners() {
    addListener('exampleInputClinker', 'click', function (){
        setExampleInput('clinker');
    })

    addListener('exampleInputCblaster', 'click', function (){
        setExampleInput('cblaster_search');
    })

    addListener('toggleHelpButton', 'click',
        toggleExplanationColumn
    );
}

function addGeneralListeners(){
    addHelpButtonsListeners();
    addNotificationListeners();
    addExampleButtonListeners();

    addListener('bookMarkButton', 'click', function () {
        alert('Press CTRL + D to bookmark this page');
    });

}

function addClinkerStartPointListeners(){
    addListener('fileUploadClinker', 'change',
        getGenBankFileNames
    )
}

function addCblasterSearchListeners(){
    addListener('remoteMode', 'click', function () {
        changeSearchMode('remote');
    });

    addListener('hmmMode', 'click', function (){
        changeSearchMode('hmm');
    });

    addListener('combiMode', 'click', function (){
        changeSearchMode('combi_remote');
    });

    addListener('radioFasta', 'click', function (){
        showInputOptions('file', 1);
    });

    addListener('radioNCBIEntries', 'click', function (){
        showInputOptions('ncbi_entries', 1);
    });

    addListener('searchOptionForm', 'submit',
        addRequiredSeqs
    );

    addListener('intermediate_genes', 'click', function (){
        toggleDisabled('intermediate_max_distance', 'intermediate_max_clusters');
    });

    addListener('ncbiEntriesTextArea', 'focusout',
        validateNCBIEntries
    );

    addListener('keyFunction', 'change',
        changeHitAttribute
    );

    addListener('genomeFiles', 'change',
        getGenBankFileNames
    );
}

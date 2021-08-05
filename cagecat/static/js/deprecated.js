function hasOneElementSelected(overview){
    return overview.children.length === 1 && !overview.children[0].textContent.startsWith("No");
}

// function checkCorasonButton() {
//     let elem = document.getElementById("corasonSubmit");
//     if (elem !== null){
//         let queries = document.getElementById("selectedQueriesOverview");
//         let clusters = document.getElementById("selectedClustersOverview")
//         let referenceCluster = document.getElementById("selectedReferenceCluster");
//
//         if (hasOneElementSelected(queries) && clusters.children.length >= 1 && !clusters.children[0].textContent.startsWith("No") && hasOneElementSelected(referenceCluster)){
//             elem.removeAttribute("disabled");
//         }
//         else {
//             elem.setAttribute("disabled", "disabled");
//         }
//     }
// }

window.addEventListener("message", function(e){
    let text;
    let src = e.data[0];
    let message = e.data[1]; // e.data represents the message posted by the child
    if (src === "Queries"){
        console.log(message);
    }

    //
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

// function setMultiSelectHeight() {
//     let height = $('#downStreamModulesDiv')[0].offsetHeight - 80 + 'px';
//     let ids = ['unselectedClustersSelector', 'selectedClustersSelector', 'unselectedQueriesSelector',
//     'selectedQueriesSelector']
//     // console.log(height);
//     for (let i = 0; i < ids.length; i++) {
//         let elem = $('#' + ids[i])[0];
//         if (elem !== undefined){
//             elem.style.height = '230px'
//         }
//     }
//
// }



function lastPage () {
    window.history.back();
}

function changePrevSessionType() {
    let clickedButton = event.target;
    let module = clickedButton.id.split("Prev")[0];
    let uploadSessionID = module + "UploadedSessionFile";
    let jobIDElementID = module + "EnteredJobId";
    let labelSession = module + "LabelSessionFile"

    if (clickedButton.value === "sessionFile") {
        setRequiredAndEnabled(uploadSessionID);
        document.getElementById(labelSession).classList.remove("disabled");

        removeRequiredAndEnabled(jobIDElementID);
        document.getElementById(jobIDElementID).classList.remove("invalid");
        enableOrDisableSubmitButtons(false);
    } else if (clickedButton.value === "jobID") {
        removeRequiredAndEnabled(uploadSessionID);
        document.getElementById(labelSession).classList.add("disabled");
        setRequiredAndEnabled(jobIDElementID);
        validateJobID(jobIDElementID);
    }
}
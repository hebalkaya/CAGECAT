document.addEventListener('DOMContentLoaded', function() {
    var findIntermediateGenes = document.getElementById('find_intermediate_genes');
    findIntermediateGenes.addEventListener('change', toggleFields);
    toggleFields(); // Call the function initially

    var inputTypeRadios = document.querySelectorAll('input[name="input_type"]');
    inputTypeRadios.forEach(function(radio) {
        radio.addEventListener('change', toggleInputTypeSection);
    });

    toggleInputTypeSection(); // Call the function initially
    toggleFileSection(); // Call the function initially

    var remoteInputRadios = document.querySelectorAll('input[name="remote_input_type"]');
    remoteInputRadios.forEach(function(radio) {
        radio.addEventListener('change', toggleFileSection);
    });
});

function toggleFields() {
    var checkBox = document.getElementById('find_intermediate_genes');
    var distanceField = document.getElementById('maximum_distance');
    var clustersField = document.getElementById('maximum_clusters');

    distanceField.disabled = !checkBox.checked;
    clustersField.disabled = !checkBox.checked;
}

function toggleInputTypeSection() {
    var inputType = document.querySelector('input[name="input_type"]:checked').value;
    var section = document.getElementById('inputTypeSection');
    if (inputType === 'remote' || inputType === 'remote_hmm') {
        section.style.display = 'block';
    } else {
        section.style.display = 'none';
    }

    // Update fileSection visibility
    toggleFileSection();
}

function toggleFileSection() {
    var fileRadio = document.getElementById('fileCheckbox');
    var fileSection = document.getElementById('fileSection');
    var inputTypeSectionVisible = document.getElementById('inputTypeSection').style.display !== 'none';

    if (fileRadio && fileRadio.checked && inputTypeSectionVisible) {
        fileSection.style.display = 'block';
    } else {
        fileSection.style.display = 'none';
    }
}

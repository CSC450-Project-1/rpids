/*_______________________________________________________________________________________________________________________________

 Project Name:      Response Pattern-Based Identification System (RPIDS)
 Purpose:           A Graphical User Interface (GUI) based software to assist chemists in performing principal component
                    analysis (PCA) and hierarchical clustering analysis (HCA). 
 Project Members:   Zeth Copher
                    Josh Kuhn
                    Ryan Luer
                    Austin Pearce
                    Rich Russell
 Course:         Missouri State University CSC450- Intro to Software Engineering
 Instructor:     Dr. Razib Iqbal, Associate Professor of Computer Science 
 Contact:        RIqbal@MissouriState.edu
_________________________________________________________________________________________________________________________________*/

// #_______________________________________________________
// # showAlertMessage function
// # Displays an alert message popup based on the parameters passed in 
// #
// # Return Value
// # void
// #
// # Value Parameters
// # title        string        title of the alert
// # message      string        body of the alert message
// # confirmText  string        text on confirm button of the alert
// # confirmAction function     handler to call on confirm
// # cancelAction function      handler to call on cancel
// # showCancel   bool          whether or not to show cancel button
// # icon         string        name of icon to display in alert
// #
// #___________________________________________________________
window.showAlertMessage = function showAlertMessage({ title, message, confirmText = "", confirmAction = null, cancelAction = null, showCancel = false, icon = "error" }) {
    Swal.fire({
        icon: icon,
        title: title,
        text: message,
        showCancelButton: showCancel,
        confirmButtonText: confirmText == "" ? "Ok" : confirmText
    }).then((result) => {
        if (result.isConfirmed && confirmAction) {
            confirmAction();
        } else if (cancelAction) {
            cancelAction();
        }
    })
}

// #_______________________________________________________
// # importSubmit() Function
// # Gathers data from import form, parses into form data
// # if form is valid, calls form import function window.initImport
// #
// # Return Value
// # void                       
// #

function importSubmit() {
    form = $("#import_form")
    formData = {
        // "name": form.find("[name='name']").val(),
        "dataFormat": form.find("[name='dataFormat']:checked").val(),
        "delimiter": form.find("[name='delimiterOption']:checked").val()
    }

    if (isValidForm(formData)) {
        $('#importModal').modal('hide');
        window.initImport(formData)
    }
}

// #_______________________________________________________
// # isValidForm function
// # handles validation of form data, and adds is-invalid bootstrap class if field is invalid 
// #
// # Return Value
// # void
// #
// # Value Parameters
// # formData       object      object created by importSubmit()
// #
// #___________________________________________________________
function isValidForm(formData) {
    isValid = true;
    if (!window.importPaths.label || !window.importPaths.label.length) {
        $("#import-label").addClass("is-invalid");
        $("#import-label-feedback").addClass("d-block");
        isValid = false;
    }
    if (!window.importPaths.runs || !window.importPaths.runs.length) {
        $("#import-runs").addClass("is-invalid");
        $("#import-runs-feedback").addClass("d-block");
        isValid = false;
    }
    return isValid;
}

// #_______________________________________________________
// # isToolbarVisible function
// # handles the checkbox for conditionally showing the graph toolbar
// #
// # Return Value
// # void
// #___________________________________________________________
function isToolbarVisible() {
    let checked = document.getElementById("is-toolbar-visible").checked;
    var pca_toolbar = document.querySelector('#pca-toolbar');
    var hca_toolbar = document.querySelector('#hca-toolbar');

    // Hide toolbars
    if (!checked) {
        pca_toolbar.classList.add('hidden');
        hca_toolbar.classList.add('hidden');
    } else {
        const src = document.getElementById('plotly-frame').src
        const analysis_type = src.split("/")[3];
        if (analysis_type == 'pca') pca_toolbar.classList.remove('hidden');
        else if (analysis_type == 'hca') hca_toolbar.classList.remove('hidden');
    }
}

// #_______________________________________________________
// # various handlers
// # each of these handlers correspond to elements in ./index.html
// # these handlers handle importing labels, runs, submitting the import form, and exporting
// #_______________________________________________________
$("#import-label").on('click', window.sysImportLabel)
$("#import-runs").on('click', window.sysImportRuns)
$("#import-submit").on('click', importSubmit)
$("#export-btn").on('click', window.sysExportData)

// #_______________________________________________________
// # activeTab function
// # handles switching between the analysis tabs
// #
// # Return Value
// # void
// #
// # Value Parameters
// # analysis_type       string      analysis string associated to selected tab
// #
// #___________________________________________________________
function activeTab(analysis_type) {
    var pca_tab = document.querySelector('#pca-tab');
    var hca_tab = document.querySelector('#hca-tab');

    if (analysis_type == 'pca') {
        hca_tab.classList.remove('active');
        pca_tab.classList.add('active');
        window.changeiFrameSrc('pca/2d');
    }
    else if (analysis_type == 'hca') {
        pca_tab.classList.remove('active');
        hca_tab.classList.add('active');
        window.changeiFrameSrc('hca/dendrogram');
    }
}

// #_______________________________________________________
// # main()
// # called when page loads, sets iframe to default pca 2d
// # 
// #_______________________________________________________
$(function main() {
    window.changeiFrameSrc('pca/2d');
})

/*_______________________________________________________________________________________________________________________________

 License:
 Copyright 2021 Missouri State University

 Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
 documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
 rights to use, copy, modify, merge, publish, distribute, sub-license, and/or sell copies of the Software, and to
 permit persons to whom the Software is furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
 BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
 DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
_______________________________________________________________________________________________________________________________________*/
    // Show a customizable sweet alert error message
    window.showErrorMessage = function showErrorMessage({title, message, confirmText="", confirmAction=null, cancelAction=null,showCancel=false}){
        Swal.fire({
            icon: 'error',
            title: title,
            text: message,
            showCancelButton: showCancel,
            confirmButtonText: confirmText=="" ? "Ok" : confirmText
        }).then((result) => {
            if (result.isConfirmed && confirmAction) {
                confirmAction();
            }else if(cancelAction){
                cancelAction();
            }
        })
    }

    function importSubmit() {
        form = $("#import_form")
        formData = {
            // "name": form.find("[name='name']").val(),
            "dataFormat": form.find("[name='dataFormat']:checked").val(),
            "delimiter": form.find("[name='delimiterOption']:checked").val(),
            "analType": form.find("[name='analType']").val()
        }
        
        if(isValidForm(formData)){
            $('#importModal').modal('hide');
            window.initImport(formData)
        }
    }

    $('#analType').on('change', function (e) {
        var optionSelected = $(this).find("option:selected");
        var valueSelected  = optionSelected.val();
        if(valueSelected!='') $("#analType").removeClass("is-invalid");
        else $("#analType").addClass("is-invalid");
    });

    function isValidForm(formData){
        isValid = true;
        if(formData.analType==""){
            $("#analType").addClass("is-invalid");
            isValid = false;
        }if(!window.importPaths.runs || !window.importPaths.runs.length){
            $("#import-runs").addClass("is-invalid");
            $("#import-runs-feedback").addClass("d-block");
            isValid = false;
        }
        // if(!window.importPaths.label || !window.importPaths.label.length){
        //     $("#import-label").addClass("is-invalid");
        //     $("#import-label-feedback").addClass("d-block");
        //     isValid = false;
        // }
        return isValid;
    }

    
    $("#import-label").on('click', window.sysImportLabel)
    $("#import-runs").on('click', window.sysImportRuns)
    $("#import-submit").on('click', importSubmit)
    $("#export-btn").on('click', window.sysExportData)

    function attachHandlers() {
       
       
    }

   $(function main() {
        console.log("document loaded")
        window.changeiFrameSrc();
        
        attachHandlers()

    })


    // $("#plotly-frame").on('load', function() {
    //     // Hide loading gif and show plotly plot
    //     $('#loading-gif').css('visibility', 'hidden');
    //     $('#plotly-frame').css('visibility', 'visible');
    // })
    
// let button = document.getElementById('import_label');

// button.addEventListener('click', (e) => {
//     alert("hi")
// });

        
        // ipcRenderer.on('fileData', (event, data) => { 
        //    document.write(data) 
        // }) 

        // var label_path = document.getElementById("label").files[0].path;
        // var data_paths = [];

        // let files = document.getElementById("data").files

        // var file_type = ""
        // console.log(files);
        // for(let i = 0; i < files.length; i++){
        //     // Check consistency
        //     let path = files[i].path
        //     // let type = path.substring(path.lastIndexOf('.')+1);
        //     // if (i==0){
        //     //     file_type == type;
        //     //     console.log("Standard",file_type)
        //     // }else{
        //     //     if (type!=file_type){
        //     //         console.log("Type:",type)
        //     //         console.log("File type:", file_type)
        //     //         alert("AHHH")
        //     //         break
        //     //     }
        //     // }

        //     data_paths.push(path);
        // }

        // var options = {
        //     scriptPath: path.join(__dirname, '/../engine/'),
        //     args: [label_path, JSON.stringify(data_paths)]
        // };
    
        // window.pyImportLabel(options);

    // document.addEventListener('DOMContentLoaded', function() {
    //     // document.getElementById("start_code").addEventListener("click", start_code_function);
    //     // document.getElementById("send_code").addEventListener("click", send_code_function);
    //     // document.getElementById("stop_code").addEventListener("click", stop_code_function);
    //     // document.getElementById("open_file").addEventListener("click", open_file_function);
    //     document.getElementById("import_label").addEventListener("click",  window.sysImportLabel);
    //     document.getElementById("import_runs").addEventListener("click", window.sysImportRuns);
    //     document.getElementById("import_submit").addEventListener("click", window.sysProcessImport);
    // });


    // jQuery(function() {
    //     $('#loading-gif').css('visibility', 'visible');
    //     $('#plotly-frame').css('visibility', 'hidden');
    //  })

    //Add additional handlers here

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

    function clearForm(){
        //TODO wipes out from selections on new import
    }

    function importSubmit() {

        form = $("#import_form")

        formData = {
            // "name": form.find("[name='name']").val(),
            "dataFormat": form.find("[name='dataFormat']:checked").val(),
            "analType": form.find("[name='analType']").val()
        }
        
        if(isValidForm(formData)){
            $('#importModal').modal('hide');
            window.sendImportPaths(formData)
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
        }if(!window.importPaths.label || !window.importPaths.label.length){
            $("#import-label").addClass("is-invalid");
            $("#import-label-feedback").addClass("d-block");
            isValid = false;
        }if(!window.importPaths.runs || !window.importPaths.runs.length){
            $("#import-runs").addClass("is-invalid");
            $("#import-runs-feedback").addClass("d-block");
            isValid = false;
        }
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

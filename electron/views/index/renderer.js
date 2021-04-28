        
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
    

    function clearForm(){
        //TODO wipes out from selections on new import
    }

    function importSubmit() {

        form = $("#import_form")

        formData = {
            "name": form.find("[name='name']").val(),
            "dataFormat": form.find("[name='dataFormat']:checked").val(),
            "analType": form.find("[name='analType']").val()
        }
        
        if(validateInputs()){
            window.sysProcessImport(formData)
        }

    }

    function validateInputs(){
        //TODO
        console.log("inputs 100% validate, probably")
        return true
    }

    
    $("#import_label").on('click', window.sysImportLabel)
    $("#import_runs").on('click', window.sysImportRuns)
    $("#import_submit").on('click', importSubmit)
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

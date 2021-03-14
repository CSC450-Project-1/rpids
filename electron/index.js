        
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

    document.addEventListener('DOMContentLoaded', function() {
        // document.getElementById("start_code").addEventListener("click", start_code_function);
        // document.getElementById("send_code").addEventListener("click", send_code_function);
        // document.getElementById("stop_code").addEventListener("click", stop_code_function);
        // document.getElementById("open_file").addEventListener("click", open_file_function);
        document.getElementById("import_label").addEventListener("click",  window.sysImportLabel);
        document.getElementById("import_runs").addEventListener("click", window.sysImportRuns);
    });


    // jQuery(function() {
    //     $('#loading-gif').css('visibility', 'visible');
    //     $('#plotly-frame').css('visibility', 'hidden');
    //  })

    $("#beginImport").on('click', function(){
        console.log("Begin import clicked")
    })
    
    function updateTabs() {
    }

    // $("#plotly-frame").on('load', function() {
    //     // Hide loading gif and show plotly plot
    //     $('#loading-gif').css('visibility', 'hidden');
    //     $('#plotly-frame').css('visibility', 'visible');
    // })
    
// let button = document.getElementById('import_label');

// button.addEventListener('click', (e) => {
//     alert("hi")
// });

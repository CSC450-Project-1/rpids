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

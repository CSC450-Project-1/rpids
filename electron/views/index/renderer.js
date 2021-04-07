        
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
    
    form = $("#import_form")

    function clearForm(){
        //TODO wipes out from selections on new import
        console.log("wiping form")
        form.find("input[type='text']").val("")
        
    }

    function importSubmit() {

       

        formData = {
            id: create_UUID(),
            name: form.find("[name='name']").val(),
            dataFormat: form.find("[name='dataFormat']").val(),
            analType: form.find("[name='analType']").val(),
        }
        
        if(validateInputs()){
            window.sysProcessImport(formData)
        }

        createTab(formData)
        clearForm()

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

    

    function setupTabManager() {
        $("#tab-container").on('click', function(e){

            //TODO: tab was clicked


            //Close Tab was clicked
            if ($(e.target).attr("data-tab-close") != undefined) {
                deleteTab($(e.target).parents("[data-tab-id]"))
            }


        }) //End on Click
    }


    function createTab(formData) {


            tabManager.tabContainerElement.children(".tab").removeClass('active')
            placeholderTab = tabManager.tabContainerElement.find(".tab.placeholder")
            newTab = placeholderTab.clone().appendTo(tabManager.tabContainerElement)
            newTab.removeClass("placeholder")
            newTab.addClass("active")
            newTab.find(".tab-label").text(formData.name)
            //creates a unique id for tab
            newTab.attr("data-tab-id", formData.id)
            tabManager.tabs[formData.id] = newTab
        

        if (Object.keys(tabManager.tabs) != 0) {
            tabManager.tabContentElement.removeClass("no-tabs")
        }
        // if ()
    }

    function deleteTab(tab){
        tabId = tab.data("tab-id")
        console.log("tab to be deleted")
        delete tabManager.tabs[tabId]
        tab.remove()

        if (Object.keys(tabManager.tabs) == 0) {
            tabManager.tabContentElement.addClass("no-tabs")
        }
    }

    function create_UUID(){
        var dt = new Date().getTime();
        var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = (dt + Math.random()*16)%16 | 0;
            dt = Math.floor(dt/16);
            return (c=='x' ? r :(r&0x3|0x8)).toString(16);
        });
        return uuid;
    }
    


   $(function main() {
        console.log("document loaded")
        



        attachHandlers()

        //Tab Manager for Tabs
        tabManager = {
            tabs: {},
            tabContainerElement: $("#tab-container"),
            tabContentElement: $("#tab-content")
        }

        setupTabManager()



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

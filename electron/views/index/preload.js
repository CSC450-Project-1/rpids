const {PythonShell} = require('python-shell');
const ipc = require('electron').ipcRenderer;
const exec = require('child_process').exec;
const path = require('path');
const fs = require('fs');
const execFile = require('child_process').execFile;

const ENGINE_PATH = '../../../engine/';
const IMPORT_PATH = ENGINE_PATH+'executables/import_data.exe';
const EXPORT_PATH = ENGINE_PATH+'executables/export_data.exe';
const DASH_PATH = ENGINE_PATH+'executables/dash_server.exe';
const SERVER_ADDRESS = 'http://127.0.0.1:8050/';

window.importPaths = [];
window.maxAttempts = isDev() ? 30 : 70;

window.sysImportLabel = function() {
    ipc.send('importLabel');
    ipc.on('importLabelDone', (event, path) => {
        importPaths.label = path;
        document.querySelector('#import-label-path').innerHTML = extractFilename(path);

        // Show input field is valid
        document.querySelector('#import-label').classList.remove('is-invalid');
        document.querySelector('#import-label-feedback').classList.remove('d-block');
     })
}

function extractFilename(path){
    let path_array = path.split('\\');
    let last_index = path_array.length - 1;
    return path_array[last_index].replace(/\-/g, '_');
}

window.sysImportRuns = function() {
    ipc.send('importRuns');
    ipc.on('importRunDone', (event, paths) => { 
        importPaths.runs = paths;

        if(areValidRuns()){
            // Update input field with selected path
            if(paths.length>1){
                var filenames = '';
                for (let i = 0; i < paths.length; i++) {
                    filenames += extractFilename(paths[i])+(i==paths.length-1?'':', ');
                }
                document.querySelector('#import-runs-path').innerHTML = filenames;
            }else{
                document.querySelector('#import-runs-path').innerHTML = extractFilename(paths[0]);  
            }
            // Show input field is valid
            document.querySelector('#import-runs').classList.remove('is-invalid');
            document.querySelector('#import-runs-feedback').classList.remove('d-block');
        }else{
            window.showErrorMessage({title: 'Inconsistency Detected', message: 'Please try again with consistent file types'});
            resetInputPaths({runs: true});
        }
    })
}

function resetInputPaths({label=false,runs=false}){
    if(label){
        importPaths.label = [];
        document.querySelector('#import-label-path').innerHTML = "Choose file"
    }
    if(runs){
        importPaths.runs = [];
        document.querySelector('#import-runs-path').innerHTML = "Choose file(s)";
    }
}

function areValidRuns(){
    // Check consistency of file types
    var re = /(?:\.([^.]+))?$/; // Regex for file type
    var ext = re.exec(importPaths.runs)[1];
    var is_consistent = true;

    if (importPaths.runs.length) {
        for (let i = 0; i < importPaths.runs.length; i++) {
            let test = re.exec(importPaths.runs[i])[1]
            if (test != ext) {
                is_consistent = false;
                break;
            }
            
        }
    }
    return is_consistent;
}

function initStartServer(){
    startServer();
    checkServerStatus(1);
}

function updateLoadingGif(visible=false){
    let val = visible ? 'visible' : 'hidden';
    $('#loading-gif').css('visibility', val);
}

window.restartServer = function(){
    updateLoadingGif(true);
    checkServerStatus(1);
}

window.cancelServerRequest = function(){
    updateLoadingGif(false);
}

// Recursive method used to determine when server is done loading
function checkServerStatus(attempt_num){
    if(attempt_num==maxAttempts){
        window.showErrorMessage({title: 'Failed Starting Server',
                                 message: 'Do you want to try again?',
                                 confirmText: 'Try Again',
                                 confirmAction: window.restartServer,
                                 cancelAction: window.cancelServerRequest,
                                 showCancel: true
                                });
    }else{
        fetch('http://127.0.0.1:8050')
        .then(response => {
            if (!response.ok) {
                checkServerStatus(++attempt_num);
            }else{
                updateLoadingGif(false);
                // Reload iframe
                document.getElementById('plotly-frame').src = document.getElementById('plotly-frame').src
            }
        })
        .catch(error => {
            checkServerStatus(++attempt_num);
        });
    }
}

window.sysExportData = function() {
    ipc.send('exportData');
    ipc.on('exportDone', (event, exportPath) => { 
        if(isDev()){
            var options = {
                scriptPath: path.join(__dirname, ENGINE_PATH),
                args: [exportPath],
                pythonPath: 'python'
            };
            PythonShell.run('export_data.py', options, function (err, results) {
                if (err) throw err;
                console.log('results: ', results);
            });
        }else{
            var opt = function(){
                execFile(path.join(__dirname, EXPORT_PATH), [exportPath], function(err, results) {  
                  console.log(err)
                  console.log(results.toString());                       
              });  
            }
            opt();
        }
     })

    console.log("Export has been called");
}

function resetImportForm(){
    // Reset previously selected values for next import
    resetInputPaths({label: true,runs: true})

    $("#analType").val('');
    $('input:radio[name=dataFormat]')[0].checked = true;
}

function getSettings(){
    return new Promise(function(resolve, reject) {
        ipc.invoke('getSettings').then((result) => {
            resolve(result)
        })
    })
}

function updateSettings(settings){
    ipc.send('updateSettings', {
        settings: settings
    })
}

window.changeiFrameSrc = function changeiFrameSrc(route=false){
    if(!route){
        getSettings().then((data)=>{
            const settings = data;
            if ("analysis_type" in settings){
                let analysis_type = settings['analysis_type'];
    
                route = analysis_type=='pca' ? 'pca/2d' : 'hca/dendrogram';
                var iframe = document.getElementById('plotly-frame');
                iframe.src = SERVER_ADDRESS+route;
                showToolBar(route);
            }
        });
    }else{
        var iframe = document.getElementById('plotly-frame');
        iframe.src = SERVER_ADDRESS+route;
        showToolBar(route)
    }
}

// Show/hide toolbar of buttons based on analysis type
function showToolBar(route){
    if(route.includes('pca')){
        document.querySelector('#pca-toolbar').classList.remove('hidden');
        document.querySelector('#hca-toolbar').classList.add('hidden');
    }else if(route.includes('hca')){
        document.querySelector('#hca-toolbar').classList.remove('hidden');
        document.querySelector('#pca-toolbar').classList.add('hidden');
    }
}

window.initImport = function initImport(importFormData) {
    checkServer().then(()=>{
        console.log('Server is running');
        sendImportPaths(importFormData);
    }).catch(()=>{
        updateLoadingGif(true);
        sendImportPaths(importFormData);
    })
}

function sendImportPaths(importFormData){
    getSettings().then((data)=>{
        // Save the analysis type to the settings
        var settings = data;
        settings['analysis_type'] = importFormData.analType;
        updateSettings(settings);
    
        changeiFrameSrc();
        importData(importFormData);
    })
}

function checkServer(){
    return new Promise(function (resolve, reject){
        fetch('http://127.0.0.1:8050')
        .then(response => {
            resolve(response.ok);
        })
        .catch(error => {
            reject(error);
        });
    })
}

function importData(importFormData){
    if (importPaths.label == undefined) importPaths.label = ""
    if(isDev()){
        var options = {
            scriptPath: path.join(__dirname, ENGINE_PATH),
            args: [importPaths.label, JSON.stringify(importPaths.runs), JSON.stringify(importFormData)],
            pythonPath: 'python'
        };
        PythonShell.run('import_data.py', options, function (err, results) {
            if (err) throw err; // TODO SHOW A SWEETALERT ERROR HERE
            console.log('results: ', results);
            document.getElementById('plotly-frame').src = document.getElementById('plotly-frame').src;
        });
        resetImportForm();
        checkServer().then(()=>{
            console.log('Server is running');
        }).catch(()=>{
            initStartServer();
        })
    }else{
        var opt = function(){
            execFile(path.join(__dirname, IMPORT_PATH), [importPaths.label, JSON.stringify(importPaths.runs), JSON.stringify(importFormData)], function(err, results) {  
              console.log(err)
              console.log(results.toString());   
              initStartServer();                    
          });  
        }
        opt();
    }
}

function startServer(){
    if(isDev()){
        var options = {
            scriptPath: path.join(__dirname, '../../../engine/'),
            pythonPath: 'python'
        };

        PythonShell.run('dash_server.py', options, function (err, results) {
            if (err) throw err; // TODO: Better handling of backend/Python errors
            console.log('results: ', results);
        });
    }else{
        var opt = function(){
            execFile(path.join(__dirname, DASH_PATH), function(err, results) {  
              console.log(err)
              console.log(results.toString());                       
            });
        }
        opt();
    }

}

// Check if the app is currently in development mode
function isDev(){
    return (ipc.sendSync('isDevRequest'))
}

ipc.on('shutdownInit', function (event) {
    // Make request to shutdown dash server
    $.ajax({
        url: "http://127.0.0.1:8050/shutdown",
        type: 'GET',
    })
    ipc.send('shutdownDone');
});
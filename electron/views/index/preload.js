const {PythonShell} = require('python-shell');
const ipc = require('electron').ipcRenderer;
const exec = require('child_process').exec;
const path = require('path');
const fs = require('fs');
const execFile = require('child_process').execFile;

const ENGINE_PATH = '../../../engine/';
const EXTRA_PATH = path.join(path.dirname(process.resourcesPath), 'resources');
const IMPORT_PATH = path.join(EXTRA_PATH,'import_data.exe');
const EXPORT_PATH =  path.join(EXTRA_PATH,'/export_data.exe');
const DASH_PATH =  path.join(EXTRA_PATH,'dash_server', 'dash_server.exe');
const TEMP_PATH = path.join(__dirname, '../../../temp/')
const SERVER_ADDRESS = 'http://127.0.0.1:8050/';

window.importPaths = [];
window.maxAttempts = isDev() ? 30 : 50;

window.sysImportLabel = function() {
    if(!isDialogOpened()){
        ipc.send('importLabel');
        ipc.on('importLabelDone', (event, path) => {
            importPaths.label = path;
            document.querySelector('#import-label-path').innerHTML = extractFilename(path);
    
            resetImportValidation({label: true})
         })
    }else{
        window.showAlertMessage({title: 'Opened Dialog Detected', message: 'Please close other dialog windows and try again', icon: 'info'});
    }
}

function extractFilename(path){
    let path_array = path.split('\\');
    let last_index = path_array.length - 1;
    return path_array[last_index].replace(/\-/g, '_');
}

function resetImportForm(){
    // Reset previously selected values for next import
    resetInputPaths({label: true, runs: true})
    resetImportValidation({analType: true, label: true, runs: true});

    $("#analType").val('');
    $('input:radio[name=dataFormat]')[0].checked = true;
    $('input:radio[name=delimiterOption]')[0].checked = true;
}

window.sysImportRuns = function() {
    if(!isDialogOpened()){
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
                resetImportValidation({runs: true})
            }else{
                window.showAlertMessage({title: 'Inconsistency Detected', message: 'Please try again with consistent file types'});
                resetInputPaths({runs: true});
            }
        })
    }else{
        window.showAlertMessage({title: 'Opened Dialog Detected', message: 'Please close other dialog windows and try again', icon: 'info'});
    }
}

function resetImportValidation({analType=false, label=false, runs=false}){
        // Show input fields are valid
        if(analType){
            document.querySelector('#analType').classList.remove('is-invalid');
        }
        if(runs){
            document.querySelector('#import-runs').classList.remove('is-invalid');
            document.querySelector('#import-runs-feedback').classList.remove('d-block');
        }
        if(label){
            document.querySelector('#import-label').classList.remove('is-invalid');
            document.querySelector('#import-label-feedback').classList.remove('d-block');
        }
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
        window.showAlertMessage({title: 'Failed Starting Server',
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
    console.log("Export has been called");
    if(!isDialogOpened()){
        ipc.send('exportData');
        ipc.on('exportDone', (event, exportPath) => { 
            if(isDev()){
                var options = {
                    scriptPath: path.join(__dirname, ENGINE_PATH),
                    args: [exportPath, TEMP_PATH],
                    pythonPath: 'python'
                };
                PythonShell.run('export_data.py', options, function (err, results) {
                    if(err){
                        window.showAlertMessage({title: 'Export Error', message: 'There was a problem exporting session data'});
                        console.error(err)
                    }
                    else {
                        window.window.showAlertMessage({title: 'Export Successful', message: 'The session data has been exported successfully', icon: 'success'});                   
                        if(results) console.log('Results from export: ', results);
                    }
                });
            }else{
                var opt = function(){
                    execFile(EXPORT_PATH, [exportPath, TEMP_PATH], function(err, results) {  
                      if(err) {
                          window.showAlertMessage({title: 'Export Error', message: 'There was a problem exporting session data'});
                          console.error(err)
                      }
                      else {
                          window.showAlertMessage({title: 'Export Success', message: 'The session data has been exported successfully', icon: 'success'});
                          if(results) console.log('Results from export: ', results.toString());
                      }
                  });  
                }
                opt();
            }
         })
    }else{
        window.showAlertMessage({title: 'Opened Dialog Detected', message: 'Please close other dialog windows and try again', icon: 'info'});
    }
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
    var m;
    if (importPaths.label == undefined) importPaths.label = ""
    if(isDev()){
        var options = {
            scriptPath: path.join(__dirname, ENGINE_PATH),
            args: [importPaths.label, JSON.stringify(importPaths.runs), JSON.stringify(importFormData), TEMP_PATH],
            pythonPath: 'python'
        };
        PythonShell.run('import_data.py', options, function (err, results) {
            if(results){
                if (results[0].includes("number of passed names")){
                    m = "value error"
                }
                window.showAlertMessage({title: 'Error Occured During Import Process', message: m});
            }
            document.getElementById('plotly-frame').src = document.getElementById('plotly-frame').src;
            resetImportForm();
        });
    }else{
        var opt = function(){
            execFile(IMPORT_PATH, [importPaths.label, JSON.stringify(importPaths.runs), JSON.stringify(importFormData), TEMP_PATH], function(err, results) {  
                if(err){
                    window.showAlertMessage({title: 'Import Process Error', message: "An error occured during the import process"});
                    console.error(err)
                }
                if(results) console.log('Results from import process ',results.toString());
                document.getElementById('plotly-frame').src = document.getElementById('plotly-frame').src;
                resetImportForm();              
          });
        }
        opt();
    }
    checkServer().then(()=>{
        console.log('Server is running');
    }).catch(()=>{
        initStartServer();
    })
    console.log(importFormData);
}

function startServer(){
    if(isDev()){
        var options = {
            scriptPath: path.join(__dirname, '../../../engine/'),
            args: [TEMP_PATH],
            pythonPath: 'python'
        };

        PythonShell.run('dash_server.py', options, function (err, results) {
            if(err){
                window.showAlertMessage({title: 'Dash Server Error', message: "An error occured while trying to start the Dash Server"});
                console.error(err);
            }
            if (results) console.log('Results from dash server: ', results);
        });
    }else{
        var opt = function(){
            execFile(DASH_PATH, [TEMP_PATH], function(err, results) {  
                if(err){
                    window.showAlertMessage({title: 'Dash Server Error', message: "An error occured while trying to start the Dash Server"});
                    console.error(err);
                }
                if(results) console.log('Results from dash server: ', results.toString());                       
            });
        }
        opt();
    }
    console.log('server started');

}

// Check if the app is currently in development mode
function isDev(){
    return (ipc.sendSync('isDevRequest'));
}

function isDialogOpened(){
    return (ipc.sendSync('isDialogOpenedRequest'));
}

ipc.on('shutdownInit', function (event) {
    // Make request to shutdown dash server
    changeiFrameSrc("shutdown");
    ipc.send('shutdownDone');
});
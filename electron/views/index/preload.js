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

window.importPaths = [];
window.paths = [];

window.sysImportLabel = function() {
    ipc.send('importLabel');
    ipc.on('importLabelDone', (event, path) => {
        importPaths['label'] = path;
        document.querySelector('#import_runs').disabled = false;
     })
}

window.sysImportRuns = function() {
    ipc.send('importRuns');
    ipc.on('importRunDone', (event, paths) => { 
        importPaths['runs'] = paths;
    })
}

window.sysProcessImport = function(importFormData) {
    console.log(importFormData)

    // Check consistency of file types
    var re = /(?:\.([^.]+))?$/; // Regex for file type
    var ext = re.exec(paths[0])[1];
    var is_consistent = true;

    if (paths.length>1) {
        for (let i = 1; i < paths.length; i++) {
            if (re.exec(paths[i])[1] != ext) {
                is_consistent = false;
                break;
            }
            
        }
    }

    is_consistent ? sendImportPaths(importFormData) : showErrorMessage("Inconsistency Detected", "Please try again with consistent file types");
    paths = [];

    // TODO: PUT STARTING SERVER IN CORRECT PLACE
    $('#loading-gif').css('visibility', 'visible');
    startDashServer();

    let max = isDev() ? 30 : 70;
    checkServerStatus(max, 1);
}

// Recursive method used to determine when server is done loading
function checkServerStatus(max, attempt_num){
    if(attempt_num == max) {
        ipc.send('showServerError');
        ipc.on('restartServer', (event) => {     
            checkServerStatus(max, 0);
        })
        return $('#loading-gif').css('visibility', 'hidden');
    }

    fetch('http://127.0.0.1:8050/')
    .then(response => {
        if (!response.ok) {
            checkServerStatus(max, ++attempt_num);
        }else{
            $('#loading-gif').css('visibility', 'hidden');
            location.reload();
        }
    })
    .catch(error => {
        checkServerStatus(max, ++attempt_num);
    });
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

function sendImportPaths(importFormData) {
    if(isDev()){
        var options = {
            scriptPath: path.join(__dirname, ENGINE_PATH),
            args: [importPaths.label, JSON.stringify(importPaths.runs), importFormData],
            pythonPath: 'python'
        };
        PythonShell.run('import_data.py', options, function (err, results) {
            if (err) throw err;
            console.log('results: ', results);
        });
    }else{
        var opt = function(){
            execFile(path.join(__dirname, IMPORT_PATH), [importPaths.label, JSON.stringify(importPaths.runs), importFormData], function(err, results) {  
              console.log(err)
              console.log(results.toString());                       
          });  
        }
        opt();
    }
}

function showErrorMessage(title, message) {
    // Used to show a Sweet Alert error message
    ipc.send('showError', {
        title: title,
        message: message
    })
}

function startDashServer(){
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
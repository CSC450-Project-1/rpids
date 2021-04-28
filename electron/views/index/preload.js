const {PythonShell} = require('python-shell');
const ipc = require('electron').ipcRenderer;
const exec = require('child_process').exec;
const path = require('path');
const fs = require('fs');

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

    let max = 30;
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
        var options = {
            scriptPath: path.join(__dirname, '../../../engine/'),
            args: [exportPath],
            pythonPath: 'python'
        };
        PythonShell.run('export_data.py', options, function (err, results) {
            if (err) throw err;
            console.log('results: ', results);
        });
     })

    console.log("Export has been called");
}

function sendImportPaths(importFormData) {
    var options = {
        scriptPath: path.join(__dirname, '../../../engine/'),
        args: [importPaths.label, JSON.stringify(importPaths.runs), JSON.stringify(importFormData)],
        pythonPath: 'python'
    };

    PythonShell.run('import_data.py', options, function (err, results) {
        if (err) throw err;
        console.log('results: ', results);
    });
    console.log("Import has been called");
}

function showErrorMessage(title, message) {
    // Used to show a Sweet Alert error message
    ipc.send('showError', {
        title: title,
        message: message
    })
}

function startDashServer(){
    var options = {
        scriptPath: path.join(__dirname, '../../../engine/'),
        pythonPath: 'python'
    };

    PythonShell.run('dash_server.py', options, function (err, results) {
        if (err) throw err; // TODO: Better handling of backend/Python errors
        console.log('results: ', results);
    });
}

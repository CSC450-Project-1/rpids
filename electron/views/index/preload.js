const {PythonShell} = require('python-shell');
const ipc = require('electron').ipcRenderer;
const exec = require('child_process').exec;
const path = require('path');
const fs = require('fs');
const isDev = require('electron-is-dev');
const exec = require('child_process').execFile;

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
}

function sendImportPaths(importFormData) {
    if(isDev){
        var options = {
            scriptPath: path.join(__dirname, '/../engine/'),
            args: [importPaths.label, JSON.stringify(importPaths.runs), importFormData],
            pythonPath: 'python'
        };
        PythonShell.run('import_data.py', options, function (err, results) {
            if (err) throw err;
            console.log('results: ', results);
        });
    }else{
        var opt = function(){
            exec('file.EXE', ["arg1", "arg2", "arg3"], function(err, results) {  
              console.log(err)
              console.log(results.toString());                       
          });  
        }
        opt();
    }
}

function showErrorMessage(title, message) {
    ipc.send('showError', {
        title: title,
        message: message
    })
}

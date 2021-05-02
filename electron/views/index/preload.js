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
window.maxAttempts = isDev() ? 30 : 70;

window.sysImportLabel = function() {
    ipc.send('importLabel');
    ipc.on('importLabelDone', (event, path) => {
        importPaths.label = path;
        let filename = path.replace(/^.*[\\\/]/, '');
        document.querySelector('#import-label-path').innerHTML = filename;

        // Show input field is valid
        document.querySelector('#import-label').classList.remove('is-invalid');
        document.querySelector('#import-label-feedback').classList.remove('d-block');
     })
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
                    let filename = paths[i].replace(/^.*[\\\/]/, '')
                    filenames += filename+(i==paths.length-1?'':', ');
                }
                document.querySelector('#import-runs-path').innerHTML = filenames;
            }else{
                let filename = paths[0].replace(/^.*[\\\/]/, '')
                document.querySelector('#import-runs-path').innerHTML = filename;  
            }
            // Show input field is valid
            document.querySelector('#import-runs').classList.remove('is-invalid');
            document.querySelector('#import-runs-feedback').classList.remove('d-block');
        }else{
            window.showErrorMessage({title: 'Inconsistency Detected', message: 'Please try again with consistent file types'});
            importPaths.runs = [];
            document.querySelector('#import-runs-path').innerHTML = "Choose file(s)";  
        }
    })
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
    $('#loading-gif').css('visibility', 'visible');
    startServer();
    checkServerStatus(1);
}

window.restartServer = function(){
    $('#loading-gif').css('visibility', 'visible');
    checkServerStatus(1);
}

window.cancelServerRequest = function(){
    $('#loading-gif').css('visibility', 'hidden');
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
        fetch('http://127.0.0.1:8050/')
        .then(response => {
            if (!response.ok) {
                checkServerStatus(++attempt_num);
            }else{
                $('#loading-gif').css('visibility', 'hidden');
                location.reload();
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

window.sendImportPaths = function sendImportPaths(importFormData) {
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
            initStartServer();
        });
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
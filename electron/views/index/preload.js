/*_______________________________________________________________________________________________________________________________

 Project Name:      Response Pattern-Based Identification System (RPIDS)
 Purpose:           A Graphical User Interface (GUI) based software to assist chemists in performing principal component
                    analysis (PCA) and hierarchical clustering analysis (HCA). 
 Project Members:   Zeth Copher
                    Josh Kuhn
                    Ryan Luer
                    Austin Pearce
                    Rich Russell
 Course:         Missouri State University CSC450- Intro to Software Engineering
 Instructor:     Dr. Razib Iqbal, Associate Professor of Computer Science 
 Contact:        RIqbal@MissouriState.edu
_________________________________________________________________________________________________________________________________*/
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

// #_______________________________________________________
// # window.sysImportLabel = function()
// # sends importLabel event to ipcRenderer
// # once receiving return event importLabelDone, shows in formdata the filename from extractFileName()
// # if isDialogOpened is true, instead call showAlertMessage()
// # Return Value
// # bool                         True/False if Key is found
// #___________________________________________________________
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

// #_______________________________________________________
// # extractFilename
// # this function uses regex to return the file name from the end of a path
// #
// # Return Value
// # string                         file name
// #
// # Value Parameters
// # path        string        the path to extract file name from
// #___________________________________________________________
function extractFilename(path){
    let path_array = path.split('\\');
    let last_index = path_array.length - 1;
    return path_array[last_index].replace(/\-/g, '_');
}

// #_______________________________________________________
// # resetImportForm
// # this function resets the inputs in the import form in ./index.html
// #
// # Return Value
// # void                      
// #
// #___________________________________________________________
function resetImportForm(){
    // Reset previously selected values for next import
    resetInputPaths({label: true, runs: true})
    resetImportValidation({analType: true, label: true, runs: true});

    $("#analType").val('');
    $('input:radio[name=dataFormat]')[0].checked = true;
    $('input:radio[name=delimiterOption]')[0].checked = true;
}


// #_______________________________________________________
// # window.sysImportRuns = function()
// # sends importRuns event to ipcRenderer
// # once receiving return event importRunDone, shows in formdata the filename from extractFileName()
// # if isDialogOpened is true, instead call showAlertMessage()
// # Return Value
// #___________________________________________________________
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

// #_______________________________________________________
// # resetImportValidation
// # this function resets the validation in the import form in ./index.html
// #
// # Value Parameters
// # analType        bool        whether or not an analysis type exists
// # label        bool        whether or not a label exists
// # runs        bool        whether or not runs exists
// #
// # Return Value
// # void                      
// #
// #___________________________________________________________
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


// #_______________________________________________________
// # resetInputPaths
// # this function resets the input form for files in the import form in ./index.html
// #
// # Value Parameters
// # label        bool        whether or not an analysis type exists
// # runs        bool        whether or not a label exists
// #
// # Return Value
// # void                      
// #
// #___________________________________________________________
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

// #_______________________________________________________
// # areValidRuns
// # this function checks that all the files have consistent file extensions using regex
// #
// #
// # Return Value
// # is_consistent      bool                      
// #
// #___________________________________________________________
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

// #_______________________________________________________
// # initStartServer
// # this is an initialization function which calls startServer and checkServerStatus
// #
// #
// # Return Value
// # void                      
// #
// #___________________________________________________________
function initStartServer(){
    startServer();
    checkServerStatus(1);
}

// #_______________________________________________________
// # initStartServer
// # this is an initialization function which calls startServer and checkServerStatus
// #
// #
// # Return Value
// # void                      
// #
// #___________________________________________________________
function updateLoadingGif(visible=false){
    let val = visible ? 'visible' : 'hidden';
    $('#loading-gif').css('visibility', val);
}

// #_______________________________________________________
// # restartServer
// # calls updateLoadingGif and checks the status of the server
// #
// #
// # Return Value
// # void                      
// #
// #___________________________________________________________
window.restartServer = function(){
    updateLoadingGif(true);
    checkServerStatus(1);
}

// #_______________________________________________________
// # cancelServerRequest
// # cancels the updateLoadingGif function
// #
// #
// # Return Value
// # void                      
// #
// #___________________________________________________________
window.cancelServerRequest = function(){
    updateLoadingGif(false);
}


// #_______________________________________________________
// # checkServerStatus
// # continues to send requests to server to check the status of the server, calls function attempt_num times
// #
// #
// # Value Parameters
// # attempt_num      int       number of times to recurse through the function 
//
// # Return Value
// # void                      
// #
// #___________________________________________________________

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

// #_______________________________________________________
// # sysExportData
// # sends the exportData event to ipc, upon receiving the event exportDone, executes the export python file, and displays an alert given it's results
// #
// #
//
// # Return Value
// # void                      
// #
// #___________________________________________________________
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

// #_______________________________________________________
// # sysExportData
// # sends the exportData event to ipc, upon receiving the event exportDone, executes the export python file, and displays an alert given it's results
// #
// #
//
// # Return Value
// # void                      
// #
// #___________________________________________________________
function getSettings(){
    return new Promise(function(resolve, reject) {
        ipc.invoke('getSettings').then((result) => {
            resolve(result)
        })
    })
}

// #_______________________________________________________
// # updateSettings
// # sends the updateSettings event to ipc, upon receiving the event exportDone, executes the export python file, and displays an alert given it's results
// #
// #
//
// # Return Value
// # void                      
// #
// #___________________________________________________________
function updateSettings(settings){
    ipc.send('updateSettings', {
        settings: settings
    })
}

// #_______________________________________________________
// # changeiFrameSrc
// # changes the iframe based on the route that is passed in based on the analysis type in settings, returned from getSettings()
// #
// #
// # Value Parameters
// # route       bool       whether or not there is a route passed in
// #
// # Return Value
// # void                      
// #
// #___________________________________________________________

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


// #_______________________________________________________
// # showToolBar
// # changes css stylings of the toolbar based on the type of analysis shown
// #
// #
// # Value Parameters
// # route       string       type of route that is being used by the dash server
// #
// # Return Value
// # void                      
// #
// #___________________________________________________________
function showToolBar(route){
    if(route.includes('pca')){
        document.querySelector('#pca-toolbar').classList.remove('hidden');
        document.querySelector('#hca-toolbar').classList.add('hidden');
    }else if(route.includes('hca')){
        document.querySelector('#hca-toolbar').classList.remove('hidden');
        document.querySelector('#pca-toolbar').classList.add('hidden');
    }
}

// #_______________________________________________________
// # initImport
// # checks if the server is running, and calls sendImportPaths with importFormData, otherwise calls updateLoadingGif
// #
// #
// # Value Parameters
// # importFormData       JSON       form data from the import form
// #
// # Return Value
// # void                      
// #
// #___________________________________________________________

window.initImport = function initImport(importFormData) {
    checkServer().then(()=>{
        console.log('Server is running');
        sendImportPaths(importFormData);
    }).catch(()=>{
        updateLoadingGif(true);
        sendImportPaths(importFormData);
    })
}

// #_______________________________________________________
// # initImport
// # checks if the server is running, and calls sendImportPaths with importFormData, otherwise calls updateLoadingGif
// #
// #
// # Value Parameters
// # importFormData       JSON       form data from the import form
// #
// # Return Value
// # void                      
// #
// #___________________________________________________________

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


// #_______________________________________________________
// # initImport
// # checks if the server is running, and calls sendImportPaths with importFormData, otherwise calls updateLoadingGif
// #
// #
// # Value Parameters
// # importFormData       JSON       form data from the import form
// #
// # Return Value
// # void                      
// #
// #___________________________________________________________

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


// #_______________________________________________________
// # importData
// # uses the passed in importFormData to execute the import python business layer script, changed the plotly source, and resets the import form
// #
// #
// # Value Parameters
// # importFormData       JSON       form data from the import form
// #
// # Return Value
// # void                      
// #
// #___________________________________________________________

function importData(importFormData){
    if (importPaths.label == undefined) importPaths.label = ""
    if(isDev()){
        var options = {
            scriptPath: path.join(__dirname, ENGINE_PATH),
            args: [importPaths.label, JSON.stringify(importPaths.runs), JSON.stringify(importFormData), TEMP_PATH],
            pythonPath: 'python'
        };
        PythonShell.run('import_data.py', options, function (err, results) {
            var m = "default error";
            if(results){
                if (results[0].includes("Oops! <class 'ValueError'>")){
                    m = "Please select the correct format of the data and retry."
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
}

// #_______________________________________________________
// # startServer
// # attempts to start the dash server, executing the Dash Server business layer script.
// #
// #
// #
// # Return Value
// # void                      
// #
// #___________________________________________________________
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

}

// #_______________________________________________________
// # isDev
// # Check if the app is currently in development mode
// #
// #
// #
// # Return Value
// # void                      
// #
// #___________________________________________________________

function isDev(){
    return (ipc.sendSync('isDevRequest'));
}

// #_______________________________________________________
// # isDialogOpened
// # Check if the app is current displaying a dialog, like an alert
// #
// #
// #
// # Return Value
// # bool                      
// #
// #___________________________________________________________

function isDialogOpened(){
    return (ipc.sendSync('isDialogOpenedRequest'));
}

// #_______________________________________________________
// # shutdownInit event handler
// # changes the iframe source to the shutdown route, and sends the event shutdownDone to ipc.
// #
// #
// #
// # Return Value
// # void                      
// #
// #___________________________________________________________
ipc.on('shutdownInit', function (event) {
    // Make request to shutdown dash server
    changeiFrameSrc("shutdown");
    ipc.send('shutdownDone');
});

/*_______________________________________________________________________________________________________________________________

 License:
 Copyright 2021 Missouri State University

 Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
 documentation files (the "Software"), to deal in the Software without restriction, including without limitation the 
 rights to use, copy, modify, merge, publish, distribute, sub-license, and/or sell copies of the Software, and to
 permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
 BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
 NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
 DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
_______________________________________________________________________________________________________________________________________*/
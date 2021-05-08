/*_______________________________________________________________________________________________________________________________

 Project Name:      Response Pattern-Based Identification System (RPIDS)
 Purpose:           A Graphical User Interface (GUI) based software to assist chemists in performing principal component
                    analysis (PCA) and hierarchical clustering analysis (HCA). 
 Project Members:   Zeth Copher
                    Josh Kuhn
                    Ryan Luer
                    Austin Pearce
                    Rich Russell
 Course:         Missouri State University CSC450 - Intro to Software Engineering Spring 2021
 Instructor:     Dr. Razib Iqbal, Associate Professor of Computer Science 
 Contact:        RIqbal@MissouriState.edu

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


const ipc = require('electron').ipcRenderer;
const path = require('path');
const fs = require('fs');

window.sysGetSettings = function(){
    var settings = {};
    ipc.invoke('getSettings').then((result) => {
        settings = result;
    })
    return settings;
}

window.sysUpdateSettings = function(settings){
    ipc.send('updateSettings', {
        settings: settings
    })
}

window.sysImportProject = function() {
    ipc.send('importProject');
    ipc.on('importProjectDone', (event, path) => {
        //TODO: SEND PATH TO PYTHON FOR IMPORTING PROJECT
    })
}

window.sysGetVersion = function(){
    // Get app version from package file
    let package_raw = fs.readFileSync(path.resolve(__dirname, '../../../package.json'));
    let package = JSON.parse(package_raw);
    return package["version"];
}

window.sysCreateMainWindow = function(){
    ipc.send('createWindow');
}

window.sysCloseApp = function(){
    ipc.send('closeApp');
}
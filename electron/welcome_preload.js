const ipc = require('electron').ipcRenderer;
const path = require('path');
const fs = require('fs');

window.sysGetSettings = function(){
    const settings = {};
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
    let package_raw = fs.readFileSync(path.resolve(__dirname, '../package.json'));
    let package = JSON.parse(package_raw);
    return package["version"];
}

window.sysCreateMainWindow = function(){
    ipc.send('createWindow');
}

window.sysCloseApp = function(){
    ipc.send('closeApp');
}
// Modules to control application life and create native browser window
const { app, BrowserWindow, ipcMain, Notification, dialog } = require("electron");
const {PythonShell} = require('python-shell');
const exec = require('child_process').exec;
const path = require('path')
const Swal = require("electron-alert");

var nodeConsole = require('console');
var my_console = new nodeConsole.Console(process.stdout, process.stderr);
var child;

function print_both(str) {
    console.log('main.js:    ' + str);
    my_console.log('main.js:    ' + str);
}

function createWindow() {
    // Create the browser window.
    const mainWindow = new BrowserWindow({
        width: 820,
        height: 650,
        icon: __dirname+'/logo.ico',
        resizable: true,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: false,
            nodeIntegration: false
        }
    })

    // and load the index.html of the app.
    mainWindow.loadFile('./electron/index.html');

    // Open the DevTools.
    mainWindow.webContents.openDevTools()

    var options = {
        scriptPath: path.join(__dirname, '/../engine/'),
        pythonPath: 'python'
    };

    // Start Dash server
    PythonShell.run('dash_server.py', options, function (err, results) {
        if (err) throw err; // TODO: Better handling of backend/Python errors
        console.log('results: ', results);
    });
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
    createWindow();

    app.on('activate', function() {
        // On macOS it's common to re-create a window in the app when the
        // dock icon is clicked and there are no other windows open.
        if (BrowserWindow.getAllWindows().length === 0) createWindow()
    });
});

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', function() {
    if (process.platform !== 'darwin') app.quit();
});

// Show window for importing label file
ipcMain.on('importLabel', (event, args) => {
    dialog.showOpenDialog({
        title: "Import Label File",
        buttonLabel: "Import",
        filters: [
            { name: 'All Files', extensions: ['csv','txt','xlsx'] }
        ],
        properties: ['openFile']
      }).then(result => {
        if(!result.canceled){
            event.sender.send('labelDone', result.filePaths[0]);
        }
      }).catch(err => {
        console.error("Error in importing label: ", err);
      });
 });

 // Show window for importing run data files
 ipcMain.on('importRuns', (event, args) => {
    dialog.showOpenDialog({
        title: "Import Run Data Files",
        buttonLabel: "Import",
        filters: [
            { name: 'All Files', extensions: ['csv','txt','xlsx'] }
        ],
        properties: ['openFile', 'multiSelections']
      }).then(result => {
        if(!result.canceled){
            event.sender.send('runDone', result.filePaths);
        }
      }).catch(err => {
        console.error("Error in importing runs: ", err);
      });
 });

 ipcMain.on('showError', (event, args) => {
    let alert = new Swal();
    let swalOptions = {
        title: args.title,
        text: args.message,
        type: "error",
    };
    
    alert.fireFrameless(swalOptions, null, true, false);
 })

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
ipcMain.on('execute', (command) => {
    console.log('executing ls');
    child = exec("ls", function(error, stdout, stderr) {
        if (error !== null) {
            console.log('exec error: ' + error);
        }
    });
});


ipcMain.on('open_json_file', () => {
    var fs = require('fs');
    var fileName = './config.json';
    var file = require(fileName);

    // Asynchronous read
    // fs.readFile('config.json', function (err, data) {
    //   if (err) {
    //     return console.error(err);
    //   }
    //   console.log("Asynchronous read: " + data.toString());
    // });

    // Synchronous read
    var data = fs.readFileSync(fileName);
    var json = JSON.parse(data);

    print_both('Called through ipc.send from gui_example.js');
    print_both('Data from config.json:\nA_MODE = ' + json.A_MODE + '\nB_MODE = ' + json.B_MODE +
        '\nC_MODE = ' + json.C_MODE + '\nD_MODE = ' + json.D_MODE);
});
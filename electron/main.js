// Modules to control application life and create native browser window
const { app, BrowserWindow, ipcMain, dialog, Menu} = require("electron");
const fs = require('fs');
const {PythonShell} = require('python-shell');
const path = require('path')
const isDev = require('electron-is-dev');
const exec = require('child_process').exec;


function createWelcomeWindow() {
    // Create the welcome browser window
    const welcomeWindow = new BrowserWindow({
        width: 920,
        height: 600,
        icon: __dirname+'../../build/icon.ico',
        resizable: true,
        webPreferences: {
            preload: path.join(__dirname, './views/welcome/preload.js'),
            contextIsolation: false,
            nodeIntegration: false
        },
        backgroundColor: '#303030',
        transparent: true,
        frame: false,
        fullscreenable: false,
        show: false
    })

    // TODO
    welcomeWindow.setMinimumSize(920, 600);

    welcomeWindow.loadFile('./electron/views/welcome/welcome.html');

    welcomeWindow.once('ready-to-show', () => {
        welcomeWindow.show()
    })
}

function createMainWindow() {
    // Create the main browser window.
    const mainWindow = new BrowserWindow({
        icon: __dirname+'../../build/icon.ico',
        resizable: true,
        webPreferences: {
            preload: path.join(__dirname, './views/index/preload.js'),
            contextIsolation: false,
            nodeIntegration: false
        },
        backgroundColor: '#303030',
        show: false,
        title: "RPIDS"
    })

    // TODO
    mainWindow.setMinimumSize(920, 600);

    // and load the index.html of the app.
    mainWindow.loadFile('./electron/views/index/index.html');

    // Open the DevTools.
    isDev && mainWindow.webContents.openDevTools();

    var options = {
        scriptPath: path.join(__dirname, '/../engine/'),
        pythonPath: 'python'
    };


    mainWindow.once('ready-to-show', () => {
        mainWindow.show()
        mainWindow.maximize()
    })

    // Close app when main window is closed
    mainWindow.once('close', () => {
        app.quit();
    })
}

function getTemplate(settings){
    if(isDev){
        const template = [
            {
               label: 'Settings',
               submenu: [
                  {
                     label: 'Show initial load window',type: 'checkbox', checked: settings["show_welcome_page"],
                     click () {
                        settings["show_welcome_page"] = !settings["show_welcome_page"];
                        updateSettings(settings);
                      }
                  },
               ]
            },
            
            {
               label: 'View',
               submenu: [
                  {
                     role: 'toggleDevTools' // TODO: REMOVE ON PRODUCTION
                  },
                  {
                     role: 'reload'
                  },
                  {
                     type: 'separator'
                  },
                  {
                     role: 'resetzoom'
                  },
                  {
                     role: 'zoomin'
                  },
                  {
                     role: 'zoomout'
                  },
                  {
                     type: 'separator'
                  },
                  {
                     role: 'togglefullscreen'
                  }
               ]
            },
            
            {
               role: 'window',
               submenu: [
                  {
                     role: 'minimize'
                  },
                  {
                     role: 'close'
                  }
               ]
            },
            
            {
               role: 'help',
               submenu: [
                  {
                     label: 'Learn More' //TODO: OPEN UP USER DOCUMENTATION
                  }
               ]
            }
         ]
         return template;
    }else{
        const template = [
            {
               label: 'Settings',
               submenu: [
                  {
                     label: 'Show initial load window',type: 'checkbox', checked: settings["show_welcome_page"],
                     click () {
                        settings["show_welcome_page"] = !settings["show_welcome_page"];
                        updateSettings(settings);
                      }
                  },
               ]
            },
            
            {
               label: 'View',
               submenu: [
                  {
                     role: 'reload'
                  },
                  {
                     type: 'separator'
                  },
                  {
                     role: 'resetzoom'
                  },
                  {
                     role: 'zoomin'
                  },
                  {
                     role: 'zoomout'
                  },
                  {
                     type: 'separator'
                  },
                  {
                     role: 'togglefullscreen'
                  }
               ]
            },
            
            {
               role: 'window',
               submenu: [
                  {
                     role: 'minimize'
                  },
                  {
                     role: 'close'
                  }
               ]
            },
            
            {
               role: 'help',
               submenu: [
                  {
                     label: 'Learn More' //TODO: OPEN UP USER DOCUMENTATION
                  }
               ]
            }
         ]
         return template
    }
}

//TODO: Add more to menu
function createMenu(settings){
    const template = getTemplate(settings);
     
     const menu = Menu.buildFromTemplate(template)
     Menu.setApplicationMenu(menu)
}

function getSettings(){
     // Check if settings.json exists. If doesn't exist, create one using settings-default template
    if(fs.existsSync(path.resolve(__dirname, '../settings.json'))) {
        let settings = fs.readFileSync(path.resolve(__dirname, '../settings.json'));
        return JSON.parse(settings);
    }else{
        let settings = fs.readFileSync(path.resolve(__dirname, '../settings-default.json'));
        fs.writeFileSync(path.resolve(__dirname, '../settings.json'), settings, function (err) {
            if (err) throw err;
        });
        return JSON.parse(settings);
    }
}

function updateSettings(new_settings){
    fs.writeFileSync(path.resolve(__dirname, '../settings.json'), JSON.stringify(new_settings));
}

// Listen for get settings channel request
ipcMain.handle('getSettings', async (event) => {
    return getSettings();
})

ipcMain.on('updateSettings', (event, args) => {
    const new_settings = args.settings;
    updateSettings(new_settings);
});


// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
    const settings = getSettings();

    createMenu(settings);
    settings["show_welcome_page"] ? createWelcomeWindow() : createMainWindow();

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
            event.sender.send('importLabelDone', result.filePaths[0]);
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
            event.sender.send('importRunDone', result.filePaths);
        }
    }).catch(err => {
        console.error("Error in importing runs: ", err);
    });
});


// TODO: Called when initiated a new project
ipcMain.on('createWindow', (event, args) => {
    var welcomeWindow = BrowserWindow.getFocusedWindow();
    welcomeWindow.hide();

    const settings = getSettings();

    createMenu(settings);
    createMainWindow();
});

ipcMain.on('importProject', (event, args) => {
    dialog.showOpenDialog({
        title: "Import Project File",
        buttonLabel: "Import",
        filters: [
            { name: 'All Files', extensions: ['csv'] }
        ],
        properties: ['openFile']
    }).then(result => {
        if(!result.canceled){
            event.sender.send('importProjectDone', result.filePaths[0]);
        }
    }).catch(err => {
        console.error("Error in importing project: ", err);
    });
});

// Close window
ipcMain.on('closeApp', (event, args) => {
    quitApp();
});

ipcMain.on('exportData', (event, args)=> {
    dialog.showSaveDialog({
        title: "Export Data File",
        buttonLabel: "Export",
        filters: [
            { name: '.csv', extensions: ['csv'] }
        ],
        // properties: ['openDirectory']
      }).then(result => {
            event.sender.send('exportDone', result.filePath);
      }).catch(err => {
        console.error("Error in exporting data: ", err);
      });
 });

ipcMain.on('isDevRequest', (event, args) => {
    event.returnValue = isDev;
 })

app.on('before-quit', (event, args) => {
    event.preventDefault();
    quitApp();
})

function quitApp(){
    const win = BrowserWindow.getFocusedWindow();
    if(win && win.title=="RPIDS"){
        // Close dash server instance
        win.webContents.send('shutdownInit');
        ipcMain.on('shutdownDone', (event, args) => {
            app.exit();
        })
    }else{
        app.exit();
    }
}

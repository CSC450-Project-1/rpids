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


// Modules to control application life and create native browser window
const { app, BrowserWindow, ipcMain, dialog, Menu, shell} = require("electron");
const fs = require('fs');
const path = require('path')
const isDev = require('electron-is-dev');

isDialogOpened = false;

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

    welcomeWindow.setMinimumSize(920, 600); // TODO

    welcomeWindow.loadFile('./electron/views/welcome/welcome.html');

    welcomeWindow.webContents.on('did-finish-load', () => {
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

    mainWindow.setMinimumSize(920, 600); // TODO

    // Load the index.html of the app
    mainWindow.loadFile('./electron/views/index/index.html');

    // Open the DevTools if in development
    isDev && mainWindow.webContents.openDevTools();

    mainWindow.webContents.on('did-finish-load', () => {
        mainWindow.show()
        mainWindow.maximize()
    })
  
    // Close app when main window is closed
    mainWindow.once('close', () => {
        mainWindow.webContents.send('shutdownInit');
        ipcMain.on('shutdownDone', (event, args) => {
            app.quit();
        })
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
                     role: 'toggleDevTools'
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
                     label: 'Learn More',
                     click () {
                        shell.openExternal("https://github.com/CSC450-Project-1/rpids");
                     }
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
    isDialogOpened = true;
    dialog.showOpenDialog({
        title: "Import Label File",
        buttonLabel: "Import",
        filters: [
            { name: 'All Files', extensions: ['csv','txt','xlsx'] }
        ],
        properties: ['openFile']
    }).then(result => {
        isDialogOpened = false;
        if(!result.canceled){
            event.sender.send('importLabelDone', result.filePaths[0]);
        }
    }).catch(err => {
        console.error("Error in importing label: ", err);
    });
});

// Show window for importing run data files
ipcMain.on('importRuns', (event, args) => {
    isDialogOpened = true;
    dialog.showOpenDialog({
        title: "Import Run Data Files",
        buttonLabel: "Import",
        filters: [
            { name: 'All Files', extensions: ['csv','txt','xlsx'] }
        ],
        properties: ['openFile', 'multiSelections']
    }).then(result => {
        isDialogOpened = false;
        if(!result.canceled){
            event.sender.send('importRunDone', result.filePaths);
        }
    }).catch(err => {
        console.error("Error in importing runs: ", err);
    });
});


// Called when initiated a new project
ipcMain.on('createWindow', (event, args) => {
    var welcomeWindow = BrowserWindow.getFocusedWindow();
    welcomeWindow.hide();

    const settings = getSettings();

    createMenu(settings);
    createMainWindow();
});

// TODO: Not fully implemented
ipcMain.on('importProject', (event, args) => {
    isDialogOpened = true;
    dialog.showOpenDialog({
        title: "Import Project File",
        buttonLabel: "Import",
        filters: [
            { name: 'All Files', extensions: ['csv'] }
        ],
        properties: ['openFile']
    }).then(result => {
        isDialogOpened = false;
        if(!result.canceled){
            event.sender.send('importProjectDone', result.filePaths[0]);
        }
    }).catch(err => {
        console.error("Error in importing project: ", err);
    });
});

// Close window
ipcMain.on('closeApp', (event, args) => {
    app.quit();
});

ipcMain.on('exportData', (event, args)=> {
    isDialogOpened = true;
    dialog.showSaveDialog({
        title: "Export Data File",
        buttonLabel: "Export",
        defaultPath: 'rpids_export',
        filters: [
            { name: '.csv', extensions: ['csv'] }
        ]
      }).then(result => {
            isDialogOpened = false;
            if(!result.canceled){
                event.sender.send('exportDone', result.filePath);
            }
      }).catch(err => {
        console.error("Error in exporting data: ", err);
      });
 });

ipcMain.on('isDevRequest', (event, args) => {
    event.returnValue = isDev;
 })

 ipcMain.on('isDialogOpenedRequest', (event, args) => {
     event.returnValue = isDialogOpened;
 })

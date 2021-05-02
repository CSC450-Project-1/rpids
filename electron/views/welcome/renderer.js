$("#create-project").on('click', function(){
    updateSettings();
    window.sysCreateMainWindow();
})

$("#import-project").on('click', function(){
    window.sysImportProject(); //TODO NEEDS TO COMPLETED
    updateSettings();
})

$("#close-button").on('click', function(){
    window.sysCloseApp();
})

function updateSettings(){
    let checked = document.getElementById("show-welcome-page").checked;
    const settings = window.sysGetSettings();
    
    settings["show_welcome_page"] = checked;
    window.sysUpdateSettings(settings);
}

document.getElementById("version").innerHTML = window.sysGetVersion();
$('#logo').attr('draggable',false);
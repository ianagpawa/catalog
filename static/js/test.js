function startPage(){

    $.getJSON($SCRIPT_ROOT + '/playlists/JSON', function(data) {
        playlists = data["Playlists"];
        for (playlist in playlists){
            console.log(playlists[playlist])
        }
      });
};

$(document).ready(startPage);
$(document).on('page:load', startPage);

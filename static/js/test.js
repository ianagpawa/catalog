function startPage(){
    $.getJSON($SCRIPT_ROOT + '/playlists/JSON', function(data) {
        console.log(data);
      });
};

$(document).ready(startPage);
$(document).on('page:load', startPage);

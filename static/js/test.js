function startPage(){
    $("#test").text("GOT IT")
}

$(document).ready(startPage);
$(document).on('page:load', startPage);

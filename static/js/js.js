var debugbox_status = false;
$(document).ready(function(){
    $('#debugbox').css('display', debugbox_status?'block':'none');
    // add event listener to debug box
    $('#debugbox_button').click(function(){
        debugbox_status = !debugbox_status;
        $('#debugbox').css('display', debugbox_status?'block':'none');
    })
})

(function($){

    $( document ).ready(function() {
        $('.listline .collapsible').on('click', function(){
            $(this).parent().children('.content').slideToggle(200);
        });

        $('#collapsed').parent().children('.content').slideToggle(0);    // collapsing by default read notifications
    });

}(window.jQuery || window.$));

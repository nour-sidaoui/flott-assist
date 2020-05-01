
(function($){

    $( document ).ready(function() {
        $('.list_section .collapsible').on('click', function(){
            $(this).parent().children('.content').animate({
                height: "toggle",
                opacity: "toggle"
            }, 700);
        });

        $('.collapsed').parent().children('.content').slideToggle(0);    // collapsing by default read notifications
    });

}(window.jQuery || window.$));

$(document).ready(function () {

    $("button[id*='power-plus-']").on("click", function(){
        let id = $(this).attr("id").split('-')[2];
        $("#power-"+id).text(parseInt($("#power-"+id).text()) + 1) ;
    });

    $("button[id*='power-minus-']").on("click", function(){
        let id = $(this).attr("id").split('-')[2];
        $("#power-"+id).text(parseInt($("#power-"+id).text()) - 1) ;
    });

    $("button[id*='defense-plus-']").on("click", function(){
        let id = $(this).attr("id").split('-')[2];
        $("#defense-"+id).text(parseInt($("#defense-"+id).text()) + 1) ;
    });

    $("button[id*='defense-minus-']").on("click", function(){
        let id = $(this).attr("id").split('-')[2];
        $("#defense-"+id).text(parseInt($("#defense-"+id).text()) - 1) ;
    });

    $("#save-playground").on("click", function(){

    });

    $("a[id*='death-']").on("click", function(){
        let url = $(this).attr("data-remove-url");
            $.ajax({ type: 'GET', url: url, success: window.location.reload(true) });
            changeUrl($(this).attr('href'));
    });
});
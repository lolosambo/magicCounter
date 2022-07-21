$(document).ready(function () {

//    ------------------ POUR UNE SEULE CARTE ------------------------------
    function savePlayground(valueElement, url){
        let newValue= valueElement
        if(url.charAt(url.length - 1) >= 0){
            url = url.substring(0, url.length - 1) + newValue;
        }
        $.ajax({ type: 'GET', url: url });
    }

    $("button[id*='power-plus-']").on("click", function(){
        let id = $(this).attr("id").split('-')[2];
        $("#power-"+id).text(parseInt($("#power-"+id).text()) + 1) ;
        savePlayground($("#power-"+id).text(), $(this).attr("data-save-url"))
    });

    $("button[id*='power-minus-']").on("click", function(){
        let id = $(this).attr("id").split('-')[2];
        $("#power-"+id).text(parseInt($("#power-"+id).text()) - 1) ;
        savePlayground($("#power-"+id).text(), $(this).attr("data-save-url"))
    });

    $("button[id*='defense-plus-']").on("click", function(){
        let id = $(this).attr("id").split('-')[2];
        $("#defense-"+id).text(parseInt($("#defense-"+id).text()) + 1) ;
        savePlayground($("#defense-"+id).text(), $(this).attr("data-save-url"))
    });

    $("button[id*='defense-minus-']").on("click", function(){
        let id = $(this).attr("id").split('-')[2];
        $("#defense-"+id).text(parseInt($("#defense-"+id).text()) - 1) ;
        savePlayground($("#defense-"+id).text(), $(this).attr("data-save-url"))
    });

    $("a[id*='death-']").on("click", function(){
        let url = $(this).attr("data-remove-url");
        $.ajax({ type: 'GET', url: url, success: window.location.reload(true) });
    });

    //    ------------------ POUR TOUTES LES CARTES ------------------------------

    $("#power-plus-forAll").on("click", function(){
        $("span[id*='power-']").each(function(){
            $(this).text(parseInt($(this).text()) + 1);
        });
    });

    $("#power-minus-forAll").on("click", function(){
        $("span[id*='power-']").each(function(){
            $(this).text(parseInt($(this).text()) -1);
        });
    });

    $("#defense-plus-forAll").on("click", function(){
        $("span[id*='defense-']").each(function(){
            $(this).text(parseInt($(this).text()) + 1);
        });
    });

    $("#defense-minus-forAll").on("click", function(){
        $("span[id*='defense-']").each(function(){
            $(this).text(parseInt($(this).text()) -1);
        });
    });

//    ------ RESET TOUTES LES CARTES -------
    $("#reset_all_cards").on('click', function(){
        let url = $(this).attr("data-reset-url");
        $.ajax({ type: 'GET', url: url, success: window.location.reload.bind(window.location) });
    });

//  ---------- GESTION DE LA VIE ----------
    $("#life-plus").on("click", function(){
        let url = $(this).attr("data-save-url");
        $("#life-points").text(parseInt($("#life-points").text()) + 1) ;
        $.ajax({ type: 'GET', url: url });
    });

    $("#life-minus").on("click", function(){
        let url = $(this).attr("data-save-url");
        $("#life-points").text(parseInt($("#life-points").text()) - 1) ;
        $.ajax({ type: 'GET', url: url });
    });

//    -------- BIBLIOTHEQUE -----------
    $("button[id*='cardFormValid-']").on("click", function(e){
       cardId = $(this).attr("data-card-id");
       numberOfCards = $("#cardForm-" + cardId).val();
       urlToArray = $(this).attr("data-add-url").split("/");
       url = "";
       for (let i = 0; i < urlToArray.length -1 ; i++){
           url += urlToArray[i] + "/";
       }
       url = url + numberOfCards;
       $.ajax({ type: 'GET', url: url, success: window.location.reload.bind(window.location) });
    });

});
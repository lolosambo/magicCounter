$(document).ready(function () {

//    ------------------ POUR UNE SEULE CARTE ------------------------------
    function formatUrl(valueElement, url){
        if(valueElement != null){
            let newValue= valueElement
            if(url.charAt(url.length - 1) >= 0){
                url = url.substring(0, url.length - 1) + newValue;
            }
        }
        return url
    }

    $("button[id*='power-plus-']").on("click", function(){
        let id = $(this).attr("id").split('-')[2];
        $("#power-"+id).text(parseInt($("#power-"+id).text()) + 1) ;
        if($("#tapped-card-" + id).hasClass("tapped_card")){
            $("#total-damage").text(parseInt($("#total-damage").text()) + 1) ;
        }
        url = formatUrl($("#power-"+id).text(), $(this).attr("data-save-url"))
        $.ajax({ type: 'GET', url: url});
    });

    $("button[id*='power-minus-']").on("click", function(){
        let id = $(this).attr("id").split('-')[2];
        $("#power-"+id).text(parseInt($("#power-"+id).text()) - 1);
        if($("#tapped-card-" + id).hasClass("tapped_card")){
            $("#total-damage").text(parseInt($("#total-damage").text()) - 1) ;
        }
        url = formatUrl($("#power-"+id).text(), $(this).attr("data-save-url"))
        $.ajax({ type: 'GET', url: url });
    });

    $("button[id*='defense-plus-']").on("click", function(){
        let id = $(this).attr("id").split('-')[2];
        $("#defense-"+id).text(parseInt($("#defense-"+id).text()) + 1) ;
        url = formatUrl($("#defense-"+id).text(), $(this).attr("data-save-url"))
        $.ajax({ type: 'GET', url: url});
    });

    $("button[id*='defense-minus-']").on("click", function(){
        let id = $(this).attr("id").split('-')[2];
        $("#defense-"+id).text(parseInt($("#defense-"+id).text()) - 1) ;
        url = formatUrl($("#defense-"+id).text(), $(this).attr("data-save-url"))
        $.ajax({ type: 'GET', url: url});
    });

    // --------------------  DETRUIRE CREATURE ------------------------------------

    $("a[id*='death-']").on("click", function(){
        let url = $(this).attr("data-remove-url");
        $.ajax({ type: 'GET', url: url, success: window.location.reload(true) });
    });

    //    ------------------ POUR TOUTES LES CARTES ------------------------------

    $("#power-forAll-plus").on("click", function(){
        $("span[id*='power-']").each(function(){
            $(this).text(parseInt($(this).text()) + 1);
        });
        let url = $(this).attr("data-save-url");
        $.ajax({ type: 'GET', url: url});
    });

    $("#power-forAll-minus").on("click", function(){
        $("span[id*='power-']").each(function(){
            $(this).text(parseInt($(this).text()) -1);
        });
        let url = $(this).attr("data-save-url");
        $.ajax({ type: 'GET', url: url});
    });

    $("#defense-forAll-plus").on("click", function(){
        $("span[id*='defense-']").each(function(){
            $(this).text(parseInt($(this).text()) + 1);
        });
        let url = $(this).attr("data-save-url");
        $.ajax({ type: 'GET', url: url});
    });

    $("#defense-forAll-minus").on("click", function(){
        $("span[id*='defense-']").each(function(){
            $(this).text(parseInt($(this).text()) -1);
        });
        let url = $(this).attr("data-save-url");
        $.ajax({ type: 'GET', url: url});
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

//    -------- POINTS DE DEGATS -----------
    $("a[id*='attack-']").on("click", function(){
        let url = $(this).attr("data-attack-url");
        $.ajax({ type: 'GET', url: url, success: window.location.reload(true) });
    });

    $("a[id*='untap-']").on("click", function(){
        let url = $(this).attr("data-untap-url");
        $.ajax({ type: 'GET', url: url, success: window.location.reload(true) });
    });

//  --------------  ATTAQUE GENERALE -------------------
     $("#all-attack").on("click", function(){
        $("div[id*='tapped-card-']").each(function(){
            $(this).addClass("tapped-card");
        });
        let url = $(this).attr("data-attack-url");
         $.ajax({ type: 'GET', url: url, success: window.location.reload(true) });
     });

//  --------------  ATTAQUE GENERALE -------------------
     $("#all-untap").on("click", function(){
        $("div[id*='tapped-card-']").each(function(){
            $(this).removeClass("tapped-card");
        });
        let url = $(this).attr("data-untap-url");
         $.ajax({ type: 'GET', url: url, success: window.location.reload(true) });
     });
});
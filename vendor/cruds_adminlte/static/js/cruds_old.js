$(function(){
    $('select').select2();
    $('input').iCheck({
        checkboxClass: 'icheckbox_minimal-blue',
        radioClass: 'iradio_minimal-blue',
    });
    $("#id_name").focus();

    $("#id_name").autocomplete({
        delay: 600,
        minLength: 2,
        max: 10,
        scroll: true,
        source: function (request, response) {
            $.getJSON("/website/gasto/autocomplete/", request, function (data) {
                //create array for response objects
                var suggestions = [];
                //process response
                $.each(data, function (i, val) {
                    suggestions.push(val.name);
                });
                //pass array to callback
                response(suggestions);
            });
        },
        search: function () {
            $("#loading").addClass("isloading");
        },
        response: function () {
            $("#loading").removeClass("isloading");
        }
    });
    $("#id_quantity").focusout( function ()  {
        var value = $("#id_price").val();
        var quantity =  $("#id_quantity").val();
        var total = value * quantity;
        $("#id_subtotal").val(total);
    });
});
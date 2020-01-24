$(function(){
    $('#id_valor').mask('000.000.000.000.000,00', {reverse: true});
    $('#id_price').mask('000.000.000.000.000,00', {reverse: true});
    $('#id_subtotal').blur(function() {
        let price = $("#id_price").val();
        let quantity =  $("#id_quantity").val();
        price = parseFloat(price.replace(',','.'));
        let total = price * quantity;
        $("#id_subtotal").val(total);
    });
    $('#modal-dialog').on('shown.bs.modal', function () {
        $("#id_quantity").focus();
    });
    $('#id_name').focus();
    $('#id_name').autocomplete({
        delay: 600,
        minLength: 2,
        max: 10,
        scroll: true,
        source: function (request, response) {
            $.getJSON("/gasto/autocomplete/", request, function (data) {
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
    $('#id_name').focusout(function () {
        var value = $('#id_name').val();
        $('#id_slug').val(sanitizeTitle(value))
    });
    function sanitizeTitle(title) {
        var slug = "";
        // Change to lower case
        var titleLower = title.toLowerCase();
        // Letter "e"
        slug = titleLower.replace(/e|é|è|ẽ|ẻ|ẹ|ê|ế|ề|ễ|ể|ệ/gi, 'e');
        // Letter "a"
        slug = slug.replace(/a|á|à|ã|ả|ạ|ă|ắ|ằ|ẵ|ẳ|ặ|â|ấ|ầ|ẫ|ẩ|ậ/gi, 'a');
        // Letter "o"
        slug = slug.replace(/o|ó|ò|õ|ỏ|ọ|ô|ố|ồ|ỗ|ổ|ộ|ơ|ớ|ờ|ỡ|ở|ợ/gi, 'o');
        // Letter "u"
        slug = slug.replace(/u|ú|ù|ũ|ủ|ụ|ư|ứ|ừ|ữ|ử|ự/gi, 'u');
        // Letter "ç"
        slug = slug.replace(/ç/gi, 'c');
        // Letter "í"
        slug = slug.replace(/í/gi, 'i');
        // Letter "d"
        slug = slug.replace(/đ/gi, 'd');
        // Trim the last whitespace
        slug = slug.replace(/\s*$/g, '');
        // Change whitespace to "-"
        slug = slug.replace(/\s+/g, '-');

        return slug;
    };

    var timer;
    var i = 0;
    today=new Date();
    d=today.getDate();
    m=today.getMonth()+1;
    y=today.getFullYear();
    h=today.getHours().toString().length < 2 ? '0' + today.getHours().toString() : today.getHours().toString();
    min=today.getMinutes().toString().length < 2 ? '0' + today.getMinutes().toString() : today.getMinutes().toString();
    s=today.getSeconds().toString().length < 2 ? '0' + today.getSeconds().toString() : today.getSeconds().toString();
    // document.querySelector('#fieldData').innerHTML = d+"/"+m+"/"+y;
    // document.querySelector('#fieldHour').innerHTML = h+":"+min+":"+s;

    $('#start_timer').click( () => {
        // startTimer();
        let hour = h + ':' + min + ':' + s;
        // console.log(hour);
        $('#id_time_start').val(hour);
        $('#show_time_initial').html(hour);
        timer = setInterval(() => {
            $('#show_time').html(i.toString());
            i++;
            // console.log(i);
        }, 1000);
    })

    $('#end_timer').click( () => {
        stopTimer();
    })

    function stopTimer() {
        clearInterval(timer);
        hr_actual = h + ':' + min + ':' + s;
        min_conometrado = 1;
        seg_conometrado = i;
        while(seg_conometrado > 59) {
            min_conometrado++;
            seg_conometrado -= 60;
        }
        seg_conometrado = seg_conometrado.toString().length > 1 ? seg_conometrado : ("0" + seg_conometrado);
        min_conometrado = min_conometrado.toString().length > 1 ? min_conometrado : ("0" + min_conometrado);
        data_conometrada = "00:" + min_conometrado + ":" + seg_conometrado;
        novaHora = somaHora(hr_actual, data_conometrada, false);
        // console.log(data_conometrada);
        // console.log(novaHora);
        $('#show_time_result').html(novaHora);
        $('#id_time_end').val(novaHora);
        $('#id_time_total').val(data_conometrada);
    }


    function somaHora(hrA, hrB, zerarHora) {
        if(hrA.length != 8 || hrB.length != 8) return "00:00:00";

        temp = 0;
        nova_h = 0;
        nova_m = 0;
        novo_m = 0;
        novo_s = 0;

        hora1 = hrA.substr(0, 2) * 1;
        hora2 = hrB.substr(0, 2) * 1;
        minu1 = hrA.substr(3, 2) * 1;
        minu2 = hrB.substr(3, 2) * 1;
        segu1 = hrA.substr(6, 2) * 1;
        segu2 = hrB.substr(6, 2) * 1;

        temp = segu1 + segu2;
        while(temp > 59) {
                nova_m++;
                temp -= 60;
        }
        novo_s = temp.toString().length == 2 ? temp : ("0" + temp);

        temp = minu1 + minu2 + nova_m;
        while(temp > 59) {
                nova_h++;
                temp -= 60;
        }
        novo_m = temp.toString().length == 2 ? temp : ("0" + temp);

        temp = hora1 + hora2 + nova_h;
        while(temp > 23 && zerarHora) {
                temp -= 24;
        }
        nova_h = temp.toString().length == 2 ? temp : ("0" + temp);

        return nova_h + ':' + novo_m + ':' + novo_s;
    }
});
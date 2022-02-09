/* jshint ignore:start */
$(document).ready(function(){
    $(function(){
        $('#id_name').autocomplete({
            delay: 600,
            minLength: 2,
            max: 10,
            scroll: true,
            source: function (request, response) {
                $.getJSON("/gasto/autocomplete/", request, function (data) {
                    //create array for response objects
                    let suggestions = [];
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
            let value = $('#id_name').val();
            $('#id_slug').val(sanitizeTitle(value));
        });

        function sanitizeTitle(title) {
            let titleLower = title.toLowerCase();
            // Letter "e"
            let slug = titleLower.replace(/e|é|è|ẽ|ẻ|ẹ|ê|ế|ề|ễ|ể|ệ/gi, 'e');
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
        }

    });
    $('.datepickerwidget').datepicker({
        autoclose: true
    });

    $('#id_segmento').change(function (){
        const size = $('#id_parcelas_gasto-0-parcelas').length;
        if (!size) {
            $('#add-parcelas').click();
            $('#id_parcelas_gasto-0-parcelas').focus();
        }
    });

    $('#id_parcelas_gasto-0-valor_parcela').mask('000.000.000.000.000,00', {reverse: true});

    $(document).on('focusout', '#id_parcelas_gasto-0-parcelas', function() {
        const parcelas = $('#id_parcelas_gasto-0-parcelas').val();
        let add_one_month = '';
        let nro = 0;
        let nro_parcela = $('#id_parcelas_gasto-0-numero_parcela');
        nro_parcela.prop("readonly", true);
        $('id_parcelas_gasto-0-valor_parcela').focus();
        if (parcelas > 1) {
            nro = parseInt(nro_parcela.val()) + 1;
            const data_gasto = $('#id_datagasto').val();
            const year = data_gasto.split('-')[0];
            const month_current = data_gasto.split('-')[1];
            const day = data_gasto.split('-')[2];
            const convert_to_date = new Date(year, month_current, day);
            for (let n=1; n < parcelas; n++) {
                $('#add-parcelas').click();
                $('#id_parcelas_gasto-'+n+'-parcelas').val(parcelas);
                $('#id_parcelas_gasto-'+n+'-numero_parcela').val(nro);
                nro++;
                add_one_month = convert_to_date.getMonth()+n+1;
                if (add_one_month % 12 === 0) {
                    const add_year = Math.trunc(add_one_month / 12);
                    const year_new = parseInt(year) + add_year;
                    const result = new Date(year, add_one_month, day);
                    const day_next = ("0" + result.getDate()).substr(-2);
                    const next_data = year_new + "-" + add_one_month + "-" + day_next;
                    const data = $('#id_parcelas_gasto-' + n + '-data_parcela');
                    data.val(next_data);
                } else if (add_one_month > 12) {
                    const month = add_one_month - 12;
                    const add_year = Math.trunc(add_one_month / 12);
                    const year_new = parseInt(year) + add_year;
                    const result = new Date(year_new, month, day);
                    const month_next = ("0" + result.getMonth()).substr(-2);
                    const day_next = ("0" + result.getDate()).substr(-2);
                    const next_data = year_new + "-" + month_next + "-" + day_next;
                    const data = $('#id_parcelas_gasto-'+n+'-data_parcela');
                    data.val(next_data);
                } else {
                    const result = new Date(year, add_one_month, day);
                    const month_next = ("0" + result.getMonth()).substr(-2);
                    const day_next = ("0" + result.getDate()).substr(-2);
                    const next_data = year + "-" + month_next + "-" + day_next;
                    const data = $('#id_parcelas_gasto-'+n+'-data_parcela');
                    add_one_month = convert_to_date.getMonth()+n;
                    data.val(next_data);
                }
            }
        }
        const data_parcela = $('#id_parcelas_gasto-0-data_parcela');
        const data_gasto = $('#id_datagasto').val();
        const year = data_gasto.split('-')[0];
        const month_current = data_gasto.split('-')[1];
        const day = data_gasto.split('-')[2];
        const convert_to_date = new Date(year, month_current, day);
        add_one_month = convert_to_date.getMonth()+1;
        const next_month = new Date(year, add_one_month, day);
        const month_next = ("0" + next_month.getMonth()).substr(-2);
        const day_next = ("0" + next_month.getDate()).substr(-2);
        const next_data = year + "-" + month_next + "-" + day_next;
        // const datagasto = $('#id_datagasto').val();
        data_parcela.val(next_data);
    });
    $(document).on('focusout', '#id_parcelas_gasto-0-valor_parcela', function() {
        const parcelas = $('#id_parcelas_gasto-0-parcelas').val();
        const vlr_parcela = $('#id_parcelas_gasto-0-valor_parcela').val();
        for (let n=1; n < parcelas; n++) {
            $('#id_parcelas_gasto-'+n+'-valor_parcela').val(vlr_parcela);
        }
    });
});
$('#id_nro_da_parcela').prop("readonly", true);
$('#id_valor_da_parcela').mask('000.000.000.000.000,00', {reverse: true});
$(document).on('focusout', '#id_valor_da_parcela', function() {
    let parcelas = $('#id_parcelas').val();
    let valor_da_parcela = $('#id_valor_da_parcela').val();
    let valor_total = parcelas * valor_da_parcela.replace(',','.')
    $('#id_valor').val(valor_total)
});

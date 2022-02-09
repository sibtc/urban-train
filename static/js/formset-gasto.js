$(document).ready(function() {
  // Insere classe no primeiro item da parcela
  $('#id_parcelas_gasto-0-parcelas').addClass('clParcelas');
  $('#id_parcelas_gasto-0-numero_parcela').addClass('clNroParcela');
  $('#id_parcelas_gasto-0-valor_parcela').addClass('clVlrParcela');
  $('#id_parcelas_gasto-0-data_parcela').addClass('clDtParcela');
  $('#id_parcelas_gasto-0-valor_parcela').mask('000.000.000.000.000,00', {reverse: true});
});

$("#add-parcelas").click(function(ev) {
  ev.preventDefault();
  let count = $('#itens-parcelas').children().length;
  let tmplMarkup = $("#item-parcela").html();
  let compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);
  $("div#itens-parcelas").append(compiledTmpl);

  $('#id_parcelas_gasto-' + (count) + '-valor_parcela').mask('000.000.000.000.000,00', {reverse: true});
  $('#id_parcelas_gasto-TOTAL_FORMS').attr('value', count + 1);
  // $('html, body').animate({
  //     scrollTop: $("#add-parcelas").position().top-200
  // }, 800);
  $('#id_parcelas_gasto-' + (count) + '-parcelas').addClass('clParcelas'+(count));
  $('#id_parcelas_gasto-' + (count) + '-numero_parcela').addClass('clNroParcela'+(count));
  $('#id_parcelas_gasto-' + (count) + '-valor_parcela').addClass('clVlrParcela'+(count));
  $('#id_parcelas_gasto-' + (count) + '-data_parcela').addClass('clDtParcela'+(count));
});

$(document).on('focusout', '.clParcelas', function() {
  let parcelas = $('.clParcelas').val();
  if (parcelas > 1) {
    $('.clNroParcela').prop("readonly", true);
  } else {
    $('.clNroParcela').prop("readonly", false);
  }
  let datagasto = $('#id_datagasto').val();
  if (datagasto.length > 0){
    $('.clDtParcela').val(datagasto);
  }
  // let chance_to_price = $(this).attr('id').replace('quantity', 'price');
  // mask = $('#'+chance_to_price).mask('000.000.000.000.000,00', {reverse: true});
  // let price = $('#'+chance_to_price).val();
  // let chance_to_subtotal = $(this).attr('id').replace('quantity', 'subtotal');
  // let calculate = price.replace(',','.') * quantity;
  // $('#'+chance_to_subtotal).val(calculate);
});
